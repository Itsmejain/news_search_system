from flask import Flask,render_template,request,redirect,url_for
from datetime import datetime
from flask import jsonify
import json
from newsapi import NewsApiClient
import nltk
nltk.downloader.download('vader_lexicon')
import nltk
import json
from nltk.sentiment import SentimentIntensityAnalyzer
sia=SentimentIntensityAnalyzer()




app = Flask(__name__,template_folder="./templates")
# Init
newsapi = NewsApiClient(api_key='8fe82583caf741679d5bc6a1b9304e1c')

#route home api
@app.route("/")
def home():
 return render_template('index.html')

@app.route("/searchnews",methods=['POST'])
def searchnews():
    keyword =request.form.get("keyword_form")
    datestart =request.form.get("datastart_form")
    dateend = request.form.get("dataend_form")

    # print(keyword+ ' ' +datestart+' '+dateend)

    all_articles = newsapi.get_everything(q=keyword,
                                      from_param=datestart,
                                      to=dateend,
                                      language='en',
                                      sort_by='relevancy')
    data = all_articles['articles']
    # print(data)

    # return jsonify({'result':'success'})
    return render_template('newssearch.html',filtereddata=data,originaldata=data,sentimentvalue="all",keyword=keyword,datestart=datestart,dateend=dateend);

@app.route('/topheadlines',methods=['GET','POST'])
def topheadlinesmethod():
    print("top headlines function executing ")

    category = request.form.get("category_form")
    country = request.form.get('country_form')

    # print(category,country)

    top_headlines = newsapi.get_top_headlines(
                                          category=category,
                                          language='en',
                                          country=country)

    articles = top_headlines['articles']
    print(articles)
    # print('-------------------------------------------')
    
    print(type(articles))
    # print(type(articles[0]))
    # print(articles[0])
    # print('-------------------------------------------')
    
    return render_template("topheadlinespage.html",filtereddata = articles,originaldata = top_headlines,category=category,language='en',country=country,sentimentvalue="all")




@app.route('/filternews',methods=['GET','POST'])
def filternewsmethod():
    print("Filter News Method Executing ")
    
    pagename = request.form.get('pagename')
    sentimentvalue = request.form.get("sentimentvalue")
    
    if pagename == "headlinespage":
        
        category = request.form.get("categoryvalue")
        country = request.form.get('countryvalue')
        # print(category,country,pagename,sentimentvalue)


        top_headlines = newsapi.get_top_headlines(
                                            category=category,
                                            language='en',
                                            country=country)
        filteredarticles = []
        articles = top_headlines['articles']
        for i in articles:
            if(i['content'] is None):
                # print(sia.polarity_scores(i['title'])['compound'])
                v =sia.polarity_scores(i['title'])['compound']
            else:
                # print(sia.polarity_scores(i['content'])['compound'])
                v =sia.polarity_scores(i['content'])['compound']
        
            option = sentimentvalue

            if(option == 'positive'):
                if(v>0):
                    # print(v,i['title'])
                    filteredarticles.append(i)
                    # with open("sampleoutput.json", "a") as outfile:
                    #     json.dump(i, outfile)
                    #     print(i)

                # output_json.append(i)
            elif(option == 'negative'):
                if(v<0):
                    # print(v,i['title'])
                    filteredarticles.append(i)
                    # with open("sampleoutput.json", "a") as outfile:
                    #     json.dump(i, outfile)
                    #     print(i)
                # output_json.append(i)
            elif(option == 'all'):
                filteredarticles.append(i)
            else:
                if(v==0):
                    # print(v,i['title'])
                    filteredarticles.append(i)
                    # with open("sampleoutput.json", "a") as outfile:
                    #     json.dump(i, outfile)
                    #     print(i)




        
        #filter the articles based on the option 
        # for item in articles:
        #     print(item['title'])
        #     print('-----------------------------')
            


        return render_template("topheadlinespage.html",filtereddata = filteredarticles,originaldata = top_headlines,category=category,language='en',country=country,sentimentvalue=sentimentvalue)
    else:

        keyword =request.form.get("keywordvalue")
        datestart =request.form.get("datestartvalue")
        dateend = request.form.get("dateendvalue")

        # print(keyword,datestart,dateend,pagename)

        all_articles = newsapi.get_everything(q=keyword,
                                      from_param=datestart,
                                      to=dateend,
                                      language='en',
                                      sort_by='relevancy')
        filteredarticles = []
        articles = all_articles['articles']
        for i in articles:
            if(i['content'] is None):
                # print(sia.polarity_scores(i['title'])['compound'])
                v =sia.polarity_scores(i['title'])['compound']
            else:
                # print(sia.polarity_scores(i['content'])['compound'])
                v =sia.polarity_scores(i['content'])['compound']
        
            option = sentimentvalue

            if(option == 'positive'):
                if(v>0):
                    # print(v,i['title'])
                    filteredarticles.append(i)
                    # with open("sampleoutput.json", "a") as outfile:
                    #     json.dump(i, outfile)
                    #     print(i)

                # output_json.append(i)
            elif(option == 'negative'):
                if(v<0):
                    # print(v,i['title'])
                    filteredarticles.append(i)
                    # with open("sampleoutput.json", "a") as outfile:
                    #     json.dump(i, outfile)
                    #     print(i)
                # output_json.append(i)
            elif(option == 'all'):
                filteredarticles.append(i)
            else:
                if(v==0):
                    # print(v,i['title'])
                    filteredarticles.append(i)
                    # with open("sampleoutput.json", "a") as outfile:
                    #     json.dump(i, outfile)
                    #     print(i)


        return render_template('newssearch.html',filtereddata=filteredarticles,originaldata=articles,sentimentvalue=sentimentvalue,keyword=keyword,datestart=datestart,dateend=dateend);
  


if __name__ == "__main__":
 app.run()






































































































# # //THIS API WILL FETCH THE RANDOM DATA FROM THE DATASET AND DISPLAY ON UI
# @app.route('/r',methods=['GET'])
# def randomnews():
#     data = pd.read_csv("dataset/combineddataset.csv")
#     index = randrange(0, len(data)-1, 1)
#     title = data.loc[index].title
#     text = data.loc[index].text
#     # return "<p>helllo {text}</p>"
#     # return jsonify({'title': title, 'text': text})
#     return render_template('index.html', text = text)


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_files():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             # flash('No file part')
#             return 'NO FILE CHOSEN'
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             # flash('No selected file')
#             return 'NO FILE CHOSEN'
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
            
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'],"testing.jpg" ))
#             return image_processing()#render_template('/r')
#         else:
#             return 'Incorrect File Format'

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

# @app.route('/imageprocessing', methods=['GET', 'POST'])
# def image_processing():
#     # pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract" 
#     #Use above when on server
#     pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
#     IMAGEPATH = "uploads/"
#     img = "testing.jpg"
#     extractedInformation = pytesseract.image_to_string(Image.open(IMAGEPATH+img))
#     # print(extractedInformation)
#     return render_template('index.html', text = extractedInformation)




# try:
#     from PIL import Image
# except ImportError:
#     import Image
# import pytesseract

# def ocr_core(filename):
#     """
#     This function will handle the core OCR processing of images.
#     """
#     text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
#     return text

# ## CLASSIFICATION MODEL

# @app.route('/classification', methods=['GET', 'POST'])
# def news_classification():
#     if request.method == 'POST':
#       result = request.data.decode('UTF-8')
#       print(result)
#       #Here we are now getting the value of the input from flask UI

#       title = ""
#       text = result
#       a=[]
#       b=[]
#       a.append(title)
#       b.append(text)
#       data=pd.DataFrame({'title':a,'text':b})
#       list_=preprocess_RFC(data) 
#       print(data)
#       print(list_)
#       path='RFC'
#       with open(path , 'rb') as f:
#          lr = pickle.load(f)
#       print('successs')
#       p=lr.predict(list_)
#       print(p[0])
#       #TRY WITH DUMMY FAKE DATA - tested working fine
#       if p[0]==0:
#           prediction_fr = "FAKE"
#           print(prediction_fr)
#       else:
#           prediction_fr = "REAL"
#           print(prediction_fr)
#     example_embed='This string is from python'
#     # return render_template('index.html',pred =prediction_fr)
#     return prediction_fr


# def remove_stopWords(txt):
#   stopWords = stopwords.words('english')
#   stopWords.extend(['from', 'subject', 're', 'edu', 'use'])
#   result = []
#   for token in gensim.utils.simple_preprocess(txt):
#       if token not in gensim.parsing.preprocessing.STOPWORDS:
#         if len(token) > 3:
#            if  token not in stopWords:
#              result.append(token)
#   return result

# def get_list(txt):
#   list_words = []
#   for i in txt:
#       for j in i:
#           list_words.append(j)
#   new_list = len(list(set(list_words)))
#   return new_list
  
# def preprocess_RFC(data):
#   data['title_text_merged'] = data['title'] + ' ' + data['text']
#   data['tokenization'] = data['title_text_merged'].apply(remove_stopWords)
#   new_list=get_list(data.tokenization)
#   data['tokenization_merged'] = data['tokenization'].apply(lambda x: " ".join(x))   
#   return data.tokenization_merged



# @app.route('/recommendation', methods=['GET', 'POST'])
# def news_recommendation():
#     if request.method == 'POST':
#       result = request.data.decode('UTF-8')
#     #   print(result)
#     df = pd.read_csv("dataset/True.csv") 
#     features = ['text', 'subject']
#     for feature in features:
#       df[feature] = df[feature].fillna('')
#     df["combined_features"] = df.apply(combined_features, axis =1)
#     df1 = pd.DataFrame(df["combined_features"])
#     v = result
#     df1=df1.append({"combined_features":v},ignore_index=True)
#     print('Running count Vectorizer')
#     cv = CountVectorizer()
#     count_matrix = cv.fit_transform(df1["combined_features"])
#     print("Count Matrix:", count_matrix.toarray())
#     print('Running Cosine Similarity .....')
#     cosine_sim = cosine_similarity(count_matrix)
#     recommended_list = list(enumerate(cosine_sim[-1]))
#     sorted_recommended_list = sorted(recommended_list, key=lambda x:x[1], reverse=True)
#     sorted_recommended_list=sorted_recommended_list[1:]
#     i=0
#     newslist = []
#     for news in sorted_recommended_list:
#      print('news list printing ')
#      i=i+1
#      if i>11:
#         break
#      newslist.append(str(i)+'.'+df['title'][news[0]]+":\n"+(df['text'][news[0]])[:200]+"...."+"\n")
#         # print(get_title_from_indexee(movie[0])+":\n"+(df['text'][movie[0]])[:500]+"....")
#         # print()
#      print(df['title'][news[0]])
#     #  print(get_title_from_indexee(movie[0]))
#     return render_template('index.html', newslist=newslist , text = result) 
#     # return newslist

# def get_title_from_indexee(index):
#     return df['title'][index]
# def combined_features(row):
#     return row['title']+" "+row['text']+" "+row['subject']


# # print(ocr_core('images/ocr_example_1.png'))

# #for local server
# if __name__ == "__main__":
#  app.run(debug=True,port=8000)

# # import logging

# # app.logger.addHandler(logging.StreamHandler(sys.stdout))
# # app.logger.setLevel(logging.ERROR)
