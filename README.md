# Shadow2Profile
## Version: 0.1.0

Shadow2Profile is a roughness estimation tool from an image of rough surface with known illumination angle.
Surface image should be taken in Normally Viewed condition when parallel light is coming from Right to Left.
This program will first generate a shadow pattern (x coordinat v/s shadow-length) from threshold image and store in a CSV file (shadow_pattern.csv).
This data is then read to calculate best fitted roghness parameters (Average-slope and Ra).
The Ra value will be given in terms of unit length. To get the value in desired unit, multiply this by (No. of profile divisions x Actual length in desired unit).
All output data is stored in 'output.txt'.
Equivalent roughness profile data (x,y) will be saved at 'profile.csv'.

For more information please read the paper doi:....

## Installation
To install this tool on Windows machine please go to the latest [Release](https://github.com/DwaipayanDeb/Shadow2Profile/releases/tag/v0.1.0) and download the file `Shadow2Profile.exe` at a desired location and add this location to the `PATH` environment variable. Now open cmd at your working directory and type Shadow2Profile and press Enter to run the software.

Similarly, in a Linux OS machine just download the executible application file `Shadow2Profile` from [Release](https://github.com/DwaipayanDeb/Shadow2Profile/releases/tag/v0.1.0) to a desired location and add it to your system path.

If you do not wish to add it to the path, then just copy the file at the working directory.

## Use
Please refer the Help document in the `examples` folder. Also watch the [tutorial video](https://youtu.be/FbFrvSf6jAE) on YouTube: https://youtu.be/FbFrvSf6jAE 



## License
This project is distributed under [Apache License Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.txt)

Copyright: 2024 &copy; Dwaipayan Deb
