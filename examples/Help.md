
# Instructions and Notes for Surface Roughness Software

## Test Images
- There are **4 test images** in this folder which you can use to test how the software works.
- The filenames follow the format:  
  ```
  material_angle-of-incident_length-along-x-axis.jpg
  ```
- Here, **'length-along-x-axis'** refers to the known actual length of the area shown in the image along the x-axis.  
  (e.g., If you are using a photograph of a large terrain, then the 'length-along-x-axis' may be in kilometers.)

---

## Tested Minimisation Success

| Image Filename                  | No. of Profile Divisions |
|--------------------------------|---------------------------|
| iron_82.5deg_12mm.JPG          | 1                         |
| stone_82.5deg_12mm.jpg         | 5                         |
| Rough-1_80deg_19cm.jpg         | 6                         |
| Rough-2_80deg_20cm.jpg         | 4                         |

---

## Notes

1. If your image is **too big**, reduce it first using software like **GIMP**.
2. If you've tried different profile divisions but found **no success**, slice the image using software like **ImageJ** to create a new image with shorter x-length, or just take a screenshot showing a shorter known x-length.
3. To calculate the **final Ra value with units**, use:
   ```
   Final Ra = Output Ra × Number of Profile Divisions × X-length
   ```
   Example:  
   If you used 6 profile divisions and the software output Ra = 0.0012, then:  
   ```
   Final Ra = 0.0012 × 6 × 19 cm
   ```
   where **19 cm** is the x-length of the area shown in the image.
4. In a future update these processes will be automated.
5. Please read the paper with DOI: *[https://doi.org/10.1016/j.measurement.2025.118279]* for more details.
