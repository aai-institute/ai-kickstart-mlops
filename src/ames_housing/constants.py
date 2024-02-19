DATA_BASE_DIR = "data"
MODEL_BASE_DIR = "model"

AMES_HOUSING_DATA_SET_URL = "http://jse.amstat.org/v19n3/decock/AmesHousing.txt"
AMES_HOUSING_DATA_SET_SEPARATOR = "\t"

RANDOM_STATE = 42

SELECTED_FEATURES = {
    "nominal": ["ms_zoning", "lot_shape", "land_contour"],
    "ordinal": ["land_slope", "overall_qual", "overall_cond"],
    "numerical": ["lot_frontage", "lot_area", "mas_vnr_area"],
}

TARGET = "sale_price"

MLFLOW_TRACKING_URL = "http://localhost:4000"
MLFLOW_EXPERIMENT = "Ames housing price prediction"

LAKEFS_REPOSITORY = "ai-kickstart"
LAKEFS_BRANCH = "main"
