# Toku

Toku is an python application which coverts the  given image to a potrait and Color splash.
Toku means Edit in Tamil(தொகு).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to Run Toku.

```bash
pip install requirements.txt
```

## Usage

Draw a rectangle(Use right mouse button to drag) over the object in the image who needs to be extracted for portrait and Color splash.
Use left mouse button to mark the uncut area in object if any.
Rezise the image in file if the image is too big.

## CRUX
The foreground(object) is Extracted from Background the the foreground is used as mask it is then bitwise anded with the blurred background and grayscale background.
The extraction of foreground from background is done with 
> GrabCut :
>  In this algorithm, the region is drawn in accordance with the foreground, a rectangle is drawn over it. This is the rectangle that encases our main object. The region coordinates are decided over understanding the foreground mask.Then Gaussian Mixture Model(GMM) is used for modeling the foreground and the background.Then, in accordance with the data provided by the user, the GMM learns and creates labels for the unknown pixels and each pixel is clustered in terms of color statistics.(Formation of clusters)
A graph is generated from this pixel distribution where the pixels are considered as nodes and two additional nodes are added that is the Source node and Sink node. All the foreground pixels are connected to the Source node and every Background pixel is connected to the Sink node. 
Then the grap is cut or segmented into two.After the segmentation, the pixels that are connected to the Source node is labeled as foreground and those pixels which are connected to the Sink node is labeled as background. 

## Skills Used
###  Library 
![OpenCv](https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/OpenCV_Logo_with_text.png/195px-OpenCV_Logo_with_text.png)
### Language
![python](https://www.freepngimg.com/thumb/python_logo/5-2-python-logo-png-image-thumb.png)

# Sample
This an Example on this Toku.
![Example](https://i.imgur.com/50pWHOx.jpg)

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
