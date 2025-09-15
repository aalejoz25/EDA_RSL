
# Busqueda en Scopus
SCOPUS_QUERY = 'TITLE-ABS-KEY("computer vision" OR "image analysis" OR "image processing" OR "deep learning" OR "machine learning" OR "convolutional neural network" OR CNN OR "artificial intelligence") AND TITLE-ABS-KEY("nutritional quality" OR "fruit quality" OR "macronutrients" OR "micronutrients" OR "vitamin content" OR vitamins OR "mineral content" OR minerals OR carbohydrates OR proteins OR lipids OR sugars OR starch OR "nutrient composition") AND TITLE-ABS-KEY("crop yield" OR "yield prediction" OR "agricultural productivity" OR "leaf disease" OR "plant disease" OR "foliar disease" OR "plant pathology")'

# Busqueda en IEEE
IEEE_QUERY = '("Document Title":"computer vision" OR "Abstract":"computer vision" OR "Author Keywords":"computer vision" OR "Index Terms":"computer vision" OR "Document Title":"image analysis" OR "Abstract":"image analysis" OR "Author Keywords":"image analysis" OR "Index Terms":"image analysis" OR "Document Title":"image processing" OR "Abstract":"image processing" OR "Author Keywords":"image processing" OR "Index Terms":"image processing" OR "Document Title":"deep learning" OR "Abstract":"deep learning" OR "Author Keywords":"deep learning" OR "Index Terms":"deep learning" OR "Document Title":"machine learning" OR "Abstract":"machine learning" OR "Author Keywords":"machine learning" OR "Index Terms":"machine learning" OR "Document Title":"convolutional neural network" OR "Abstract":"convolutional neural network" OR "Author Keywords":"convolutional neural network" OR "Index Terms":"convolutional neural network" OR "Document Title":"CNN" OR "Abstract":"CNN" OR "Author Keywords":"CNN" OR "Index Terms":"CNN" OR "Document Title":"artificial intelligence" OR "Abstract":"artificial intelligence" OR "Author Keywords":"artificial intelligence" OR "Index Terms":"artificial intelligence") AND ("Document Title":"nutritional quality" OR "Abstract":"nutritional quality" OR "Author Keywords":"nutritional quality" OR "Index Terms":"nutritional quality" OR "Document Title":"fruit quality" OR "Abstract":"fruit quality" OR "Author Keywords":"fruit quality" OR "Index Terms":"fruit quality" OR "Document Title":"macronutrients" OR "Abstract":"macronutrients" OR "Author Keywords":"macronutrients" OR "Index Terms":"macronutrients" OR "Document Title":"micronutrients" OR "Abstract":"micronutrients" OR "Author Keywords":"micronutrients" OR "Index Terms":"micronutrients" OR "Document Title":"vitamin content" OR "Abstract":"vitamin content" OR "Author Keywords":"vitamin content" OR "Index Terms":"vitamin content" OR "Document Title":"mineral content" OR "Abstract":"mineral content" OR "Author Keywords":"mineral content" OR "Index Terms":"mineral content" OR "Document Title":"carbohydrates" OR "Abstract":"carbohydrates" OR "Author Keywords":"carbohydrates" OR "Index Terms":"carbohydrates" OR "Document Title":"proteins" OR "Abstract":"proteins" OR "Author Keywords":"proteins" OR "Index Terms":"proteins" OR "Document Title":"lipids" OR "Abstract":"lipids" OR "Author Keywords":"lipids" OR "Index Terms":"lipids" OR "Document Title":"sugars" OR "Abstract":"sugars" OR "Author Keywords":"sugars" OR "Index Terms":"sugars" OR "Document Title":"starch" OR "Abstract":"starch" OR "Author Keywords":"starch" OR "Index Terms":"starch" OR "Document Title":"nutrient composition" OR "Abstract":"nutrient composition" OR "Author Keywords":"nutrient composition" OR "Index Terms":"nutrient composition") AND ("Document Title":"crop yield" OR "Abstract":"crop yield" OR "Author Keywords":"crop yield" OR "Index Terms":"crop yield" OR "Document Title":"yield prediction" OR "Abstract":"yield prediction" OR "Author Keywords":"yield prediction" OR "Index Terms":"yield prediction" OR "Document Title":"agricultural productivity" OR "Abstract":"agricultural productivity" OR "Author Keywords":"agricultural productivity" OR "Index Terms":"agricultural productivity" OR "Document Title":"leaf disease" OR "Abstract":"leaf disease" OR "Author Keywords":"leaf disease" OR "Index Terms":"leaf disease" OR "Document Title":"plant disease" OR "Abstract":"plant disease" OR "Author Keywords":"plant disease" OR "Index Terms":"plant disease" OR "Document Title":"foliar disease" OR "Abstract":"foliar disease" OR "Author Keywords":"foliar disease" OR "Index Terms":"foliar disease" OR "Document Title":"plant pathology" OR "Abstract":"plant pathology" OR "Author Keywords":"plant pathology" OR "Index Terms":"plant pathology")'

# Busqueda en Web of Science
WOS_QUERY = 'TS=("computer vision" OR "image analysis" OR "image processing" OR "deep learning" OR "machine learning" OR "convolutional neural network" OR CNN OR "artificial intelligence") AND TS=("nutritional quality" OR "fruit quality" OR "macronutrients" OR "micronutrients" OR "vitamin content" OR vitamins OR "mineral content" OR minerals OR carbohydrates OR proteins OR lipids OR sugars OR starch OR "nutrient composition") AND TS=("crop yield" OR "yield prediction" OR "agricultural productivity" OR "leaf disease" OR "plant disease" OR "foliar disease" OR "plant pathology")'

# Busqueda en ScienceDirect
SD_QUERYS =  [
    'TITLE-ABSTR-KEY("computer vision" OR "deep learning") AND TITLE-ABSTR-KEY("nutritional quality" OR "fruit quality")',
    'TITLE-ABSTR-KEY("machine learning" OR "artificial intelligence") AND TITLE-ABSTR-KEY(nutrients OR proteins OR carbohydrates OR vitamins)',
    'TITLE-ABSTR-KEY("computer vision" OR "deep learning") AND TITLE-ABSTR-KEY("crop yield" OR "yield prediction")',
    'TITLE-ABSTR-KEY("machine learning" OR "artificial intelligence") AND TITLE-ABSTR-KEY("plant disease" OR "leaf disease")'
]

# Búsqueda en Google Scholar
SCHOLAR_QUERY = (
    '("artificial intelligence" OR "computer vision" OR "convolutional neural networks" OR "deep learning" OR '
    '"feature extraction" OR "image processing" OR "image segmentation" OR "machine learning" OR '
    '"recurrent neural networks" OR "transformers")'
    ' AND '
    '("fungal diseases" OR "iron chlorosis" OR "leaf spots" OR "macronutrient deficiencies" OR '
    '"micronutrient deficiencies" OR "nitrogen deficiency" OR "nutrient deficiencies" OR '
    '"phosphorus deficiency" OR "physiological disorders" OR "plant diseases" OR "plant health" OR '
    '"root rots" OR "zinc deficiency")'
    ' AND '
    '("disease detection" OR "early detection" OR "prediction" OR "real-time monitoring" OR "stress detection")'
    ' AND '
    '("amino acids" OR "carbohydrates" OR "complex carbohydrates" OR "fat-soluble vitamins" OR '
    '"functional properties" OR "macronutrients" OR "major minerals" OR "micronutrients" OR "minerals" OR '
    '"nutritional quality" OR "organoleptic properties" OR "protein content" OR "proteins" OR '
    '"simple carbohydrates" OR "trace elements" OR "vitamins" OR "water-soluble vitamins")'
)