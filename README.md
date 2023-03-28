# text style preprocessing UI

This script allows you to easily generate PNG files for every letter in a word for batch processing in Stable Diffusion. 

Similar to Adobe's last release of Text Styles, this script can help you achieve style effects on your text without having to make seperate png's. 
(you will have to postprocess the images after generating to make the words whole again though.)


I recommend using ControlNet HED to get the edges of the letters and an image size of 1024px to get the best quality, adjust the settings to get different effects.



# **Features:**

* Supports your own font .otf/.ttf files

* Allows you to control the size of the generated PNG files

* Enables you to adjust the colors of the letters and background

* Supports the use of images as overlays to put over the letters and/or background

* takes under a second to process and export the png's

# **Requirements:**

* Before using this script, ensure that you have the following dependencies installed:

* Pillow: ```pip install pillow```

* Gradio: ```pip install gradio```

# **How to use:**

* Clone the repository to your local machine and navigate to the directory.

* Install the dependencies by running the commands listed above.

* Run the script and follow the instructions displayed on the Gradio interface.

#

#### **Feel free to do a pull request or open an issue if you have any suggestions for additional features or improvements.**

#### **This script does not include integration for Stable Diffusion, there are already plenty of UIs available for that purpose.**

