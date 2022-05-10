# University of Virginia Spring 2022 Capstone Project: Fetal Heartrate Monitoring


### Data source: CTU-CHB Intrapartum Cardiotocography Database: https://physionet.org/content/ctu-uhb-ctgdb/1.0.0/

### Annotations for the data used can be found here: https://www.sciencedirect.com/science/article/pii/S2352340920305849?via%3Dihub


### Basic Usage

See `common/ipynb_tests/RecordUpdated.ipynb` for the Record class and usage of this class to create and save images of the Uterine Contraction (UC) and Fetal Heart Rate (FHR) events. This will also generate labels for each image based on 'fetal activity' taking place during the individual UC events.

See `common/ipynb_tests/4x4split_BEST_FINAL_newCTGNet_METRICS.ipynb` for the Convolutional Neural Network model implementation.
