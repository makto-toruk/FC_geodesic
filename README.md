# Comparing Functional Connectivity Matrices: <br/>A Geometry-Aware Approach applied to Participant Identification

## Data
Toy data for easy use of code is included in the `data/condition1` folder. The data includes two FC matrices (with keys `LR1` and `RL1`) of size `300 x 300` for `N=20` subjects.

## Code
The code has been tested using Python 3. Install all requirements using
```
pip3 install -r requirements.txt
```
To obtain distance matrices based on Pearson dissimilarity and Geodesic distance,
```
python3 get_dist_mtx.py -d $PWD -c1 condition1 -c2 condition1 -t demo
```
To obtain accuracy based on each distance matrix,
```
python3 get_accuracy.py -d $PWD -c1 condition1 -c2 condition1 -t demo
```
To plot the results, see `plot_results.ipynb`. (Make sure to change `HOME_DIR` to your current working directory.)

## Figures

Interactive html figures are provided for all the figures in the paper. These are particulary useful for 3D visualizations as they allow for rotation.

* [Fig 2A](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig2A.html), [Fig 2B](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig2B.html), [Fig 2C](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig2C.html), [Fig 2D](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig2D.html)
* [Fig 3](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig3.html)
* [Fig 4A_1](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig4A_1.html), [Fig 4A_2](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig4A_2.html), [Fig 4B_1](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig4B_1.html), [Fig 4B_2](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig4B_2.html)
* [Fig 5](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig5.html)
* [Fig 6A](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig6A.html), [Fig 6B](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig6B.html)
* [Fig 7A](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig7A.html), [Fig 7B](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig7B.html)
* [Fig 8](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig8.html)
* [Fig 9](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig9.html)
* [Fig 10A](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig10A.html), [Fig 10B](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig10B.html)
* [Fig 11_1](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig11_1.html), [Fig 11_2](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig11_2.html)
* [Fig 12A_1](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig12A_1.html), [Fig 12A_2](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig12A_2.html), [Fig 12B_1](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig12B_1.html), [Fig 12B_2](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig12B_2.html)
* [Fig 13_1](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig13_1.html), [Fig 13_2](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig13_2.html)
* [Fig 14A_1](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig14A_1.html), [Fig 14A_2](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig14A_2.html), [Fig 14A_3](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig14A_3.html), [Fig 14B](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig14B.html), [Fig 14C](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/Fig14C.html)
* [Fig S1](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS1.html), [Fig S2](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS2.html), [Fig S3A](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS3A.html), [Fig S3B](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS3B.html), [Fig S3C](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS3C.html), [Fig S5](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS5.html), [Fig S6](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS6.html), [Fig S7](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS7.html), [Fig S8](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS8.html), [Fig S9](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS9.html), [Fig S10](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS10.html), [Fig S11](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS11.html), [Fig S12](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS12.html), [Fig S13](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS13.html), [Fig S14](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS14.html), [Fig S15](https://htmlpreview.github.io/?https://github.com/makto-toruk/FC_geodesic/blob/master/figures/FigS15.html)
