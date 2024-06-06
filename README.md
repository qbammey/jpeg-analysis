# JPEG Compression Quality Analysis for Image Forensics and AI-Generated Content Detection

## Quentin Bammey
## Université Paris-Saclay, ENS Paris-Saclay, CNRS, Centre Borelli

This method analyses the quantization table of an image to assert whether a JPEG compression is significantly detected. Analysis on the quantization table is then performed to detect the likely JPEG quality factor of an image.

The work builds on our implementation of the JPEG quantization table estimator presented in Nikoukhah, Tina, Miguel Colom, Jean-Michel Morel, and Rafael Grompone von Gioi. "A reliable JPEG quantization table estimator." Image Processing On Line 12 (2022): 173-197.

### Citation

> Bammey, Q. (2024). JPEG Compression Quality Analysis for Image Forensics and AI-Generated Content Detection.

BibTeX:
>   @misc{jpeganalysis,
>       author = {Bammey, Quentin},
>       title = {JPEG Compression Quality Analysis for Image Forensics and AI-Generated Content Detection},
>       note = {\url{https://github.com/qbammey/jpeg-analysis}},
>       year=2024
>   }

If you use this method, you can also cite the quantization table estimator we use:
> @article{ipol.2022.399,
>    title   = {{A Reliable JPEG Quantization Table Estimator}},
>    author  = {Nikoukhah, Tina and Colom, Miguel and Morel, Jean-Michel and Grompone von Gioi, Rafael},
>    journal = {{Image Processing On Line}},
>    volume  = {12},
>    pages   = {173--197},
>    year    = {2022},
>    note    = {\url{https://doi.org/10.5201/ipol.2022.399}}
> }



### Acknowledgements

This work has received funding by the European Union under the Horizon Europe vera.ai project, grant agreement number 101070093, and by the ANR under the APATE project, grant number ANR-22-CE39-0016.
This method extends the quantization analysis of the paper by Nikoukhah, T., Colom, M., Morel, J. M., & von Gioi, R. G. (2022), A Reliable JPEG Quantization Table Estimator, IPOL. Centre Borelli is also a member of Université Paris Cité, SSA and INSERM.
