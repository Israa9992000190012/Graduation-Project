# python file to open a pickle ML model saved in my desktop
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd



with open('model/recommending_model.pkl', 'rb') as f:
    model = pickle.load(f)

# read the data
data = pd.read_csv('data/product_descriptions.csv')



# define the show_recommendations function
def show_recommendations(model, product):
    # perform the necessary transformations on the input data
    vectorizer = TfidfVectorizer(stop_words='english')
    product_descriptions1 = data.head(500)


    # use the loaded model to make predictions
    try:
        Y = vectorizer.fit_transform([product] + list(product_descriptions1['product_description']))
    except Exception as e:
        print(e)

    prediction = model.predict(Y)
   
    # return the top 5 most similar products
    return prediction



# define a function to handle user input and make predictions
def get_recommendations():
    # get user input
    user_input = input('Enter a product: ')

    # use the model to make predictions
    recommendations = show_recommendations(model, user_input)
    # the recommendations is a numpy array, so we need to convert it to a list
    recommendations = recommendations.tolist()

    # print the recommendations
    for i, recommendation in enumerate(recommendations):
        print(f'{i+1}: {recommendation}')
        if i == 10:
            break

# call the get_recommendations function to start the recommendation process
get_recommendations()