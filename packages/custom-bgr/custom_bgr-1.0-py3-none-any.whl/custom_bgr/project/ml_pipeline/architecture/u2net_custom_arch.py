import torch
import pytorch_lightning as pl
import segmentation_models_pytorch as smp
import numpy as np
import os
import pandas as pd

__all__ = ["U2NETArch"]


class U2NETArch(pl.LightningModule):
    """
    This is the model class that defines the model architecture.
    """
    def __init__(self, arch, encoder_name, in_channels, out_classes, model_dir=None, save_epochs=None, loss_func="jaccard", **kwargs):
        super().__init__()
        # Creating an instance of the 
        self.model = smp.create_model(
            arch, encoder_name=encoder_name, in_channels=in_channels, classes=out_classes, **kwargs
        )
        self.out_classes = out_classes
        # Variable chekcing if it is multiclass
        if out_classes > 2:
          self.multi_class = True
          self.loss_mode = smp.losses.MULTICLASS_MODE
        else:
          self.multi_class = False
          self.loss_mode = smp.losses.BINARY_MODE
        # print(self.multi_class, "-------------------------------")
        # preprocessing parameteres for image
        params = smp.encoders.get_preprocessing_params(encoder_name)
        self.register_buffer("std", torch.tensor(params["std"]).view(1, 3, 1, 1))
        self.register_buffer("mean", torch.tensor(params["mean"]).view(1, 3, 1, 1))

        if loss_func == "focal":
           self.loss_fn = smp.losses.FocalLoss(self.loss_mode)
        else:
           self.loss_fn = smp.losses.JaccardLoss(self.loss_mode, from_logits=True)
           
        self.best_val_iou = 0
        self.model_dir = model_dir
        self.epochs = 0
        self.save_epochs = save_epochs
        self.result_df = pd.DataFrame(columns=["epoch",'train_loss', "val_loss",'valid_per_img_iou','valid_per_dataset_iou'])
        self.train_loss = torch.tensor([0])
        self.val_loss = torch.tensor([0])
        # self.loss_fn = smp.losses.DiceLoss(self.loss_mode, from_logits=True)
        # TverskyLoss
        # self.loss_fn = smp.losses.TverskyLoss(self.loss_mode, from_logits=True, alpha=0.7, beta=0.5)
        # FocalLoss
        # self.loss_fn = smp.losses.FocalLoss(self.loss_mode)
        # LovaszLoss
        # self.loss_fn = smp.losses.LovaszLoss(self.loss_mode, from_logits=True)

    def forward(self, image):
        # normalize image here
        image = (image - self.mean) / self.std
        mask = self.model(image)
        return mask

    def shared_step(self, batch, stage):
        
        # image = batch["image"]
        image = batch[0]
        # Shape of the image should be (batch_size, num_channels, height, width)
        # if you work with grayscale images, expand channels dim to have [batch_size, 1, height, width]
        assert image.ndim == 4

        # Check that image dimensions are divisible by 32, 
        # encoder and decoder connected by `skip connections` and usually encoder have 5 stages of 
        # downsampling by factor 2 (2 ^ 5 = 32); e.g. if we have image with shape 65x65 we will have 
        # following shapes of features in encoder and decoder: 84, 42, 21, 10, 5 -> 5, 10, 20, 40, 80
        # and we will get an error trying to concat these features
        h, w = image.shape[2:]
        assert h % 32 == 0 and w % 32 == 0

        # mask = batch["mask"]
        mask = batch[1]

        # Shape of the mask should be [batch_size, num_classes, height, width]
        # for binary segmentation num_classes = 1
        assert mask.ndim == 4

        # Check that mask values in between 0 and 1, NOT 0 and 255 for binary segmentation
        # assert mask.max() <= 1.0 and mask.min() >= 0

        logits_mask = self.forward(image)
        # print(logits_mask.size(), mask.size())
        
        # Predicted mask contains logits, and loss_fn param `from_logits` is set to True

        if self.multi_class:
          mask = torch.squeeze(mask, 1) # For multiclass
        
        loss = self.loss_fn(logits_mask, mask.long())

        # Lets compute metrics for some threshold
        # first convert mask values to probabilities, then 
        # apply thresholding

        if self.multi_class:
          ## For multiclass
          prob_mask = logits_mask.softmax(dim=1)
          pred_mask = torch.argmax(prob_mask, dim=1)
          tp, fp, fn, tn = smp.metrics.get_stats(pred_mask.long(), mask.long(), mode="multiclass", num_classes=self.out_classes)
        else:
          ## For binary class
          prob_mask = logits_mask.sigmoid()
          pred_mask = (prob_mask > 0.5).float()
          tp, fp, fn, tn = smp.metrics.get_stats(pred_mask.long(), mask.long(), mode="binary")

        # We will compute IoU metric by two ways
        #   1. dataset-wise
        #   2. image-wise
        # but for now we just compute true positive, false positive, false negative and
        # true negative 'pixels' for each image and class
        # these values will be aggregated in the end of an epoch
        if stage == "train":
          self.train_loss = loss
        elif stage == "valid":
          self.val_loss = loss
        return {
            "loss": loss,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
        }

    def shared_epoch_end(self, outputs, stage):
        # aggregate step metics
        tp = torch.cat([x["tp"] for x in outputs])
        fp = torch.cat([x["fp"] for x in outputs])
        fn = torch.cat([x["fn"] for x in outputs])
        tn = torch.cat([x["tn"] for x in outputs])

        # per image IoU means that we first calculate IoU score for each image 
        # and then compute mean over these scores
        per_image_iou = smp.metrics.iou_score(tp, fp, fn, tn, reduction="micro-imagewise")
        
        # dataset IoU means that we aggregate intersection and union over whole dataset
        # and then compute IoU score. The difference between dataset_iou/conten dataset
        # and then compute IoU score. The difference between dataset_iou/content/drive/MyDrive/tablet_data/image and per_image_iou scores
        # in this particular case will not be much, however for dataset 
        # with "empty" images (images without target class) a large gap could be observed. 
        # Empty images influence a lot on per_image_iou and much less on dataset_iou.
        dataset_iou = smp.metrics.iou_score(tp, fp, fn, tn, reduction="micro")

        metrics = {
            f"{stage}_per_image_iou": per_image_iou,
            f"{stage}_dataset_iou": dataset_iou,
        }
        # print(f"{stage}_dataset_iou: ", dataset_iou)
        self.log_dict(metrics, prog_bar=True)
        return metrics

    def training_step(self, batch, batch_idx):
         
        return self.shared_step(batch, "train")      

    def training_epoch_end(self, outputs):
        self.shared_epoch_end(outputs, "train")
        return 

    def validation_step(self, batch, batch_idx):
        # print("we are here: validation_step")
        
        return self.shared_step(batch, "valid")

    def validation_epoch_end(self, outputs):
        # print("we are here:efficientnet validation_epoch_end")
        metrics = self.shared_epoch_end(outputs, "valid")
        result_to_df = [int(self.epochs), float(self.train_loss.cpu()), float(self.val_loss.cpu()), float(metrics[f"valid_per_image_iou"].cpu()), float(metrics[f"valid_dataset_iou"].cpu())]
        # print([type(self.epochs), type(self.train_loss), type(self.val_loss), type(metrics[f"valid_per_image_iou"]), type(metrics[f"valid_dataset_iou"])])
        # print(metrics[f"valid_dataset_iou"])
        if self.best_val_iou < metrics[f"valid_dataset_iou"]:
          self.best_val_iou = metrics[f"valid_dataset_iou"]
          # Saving best model 
          torch.save(self.state_dict(),f'{self.model_dir}/best.pt')
        
        if self.epochs%self.save_epochs == 0:
          torch.save(self.state_dict(),f'{self.model_dir}/epoch{self.epochs}.pt')
        self.epochs+=1
        # Saving the results csv file
        self.result_df.loc[len(self.result_df.index)] = [round(res, 3) for res in result_to_df]
        self.result_df.to_csv(self.model_dir+"/result.csv")
        return


    def test_step(self, batch, batch_idx):
        return self.shared_step(batch, "test")


    def test_epoch_end(self, outputs):
        self.shared_epoch_end(outputs, "test")
        return 

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.0001)