from modules import *
from pathlib import Path
import pandas as pd
from flask import Flask, render_template, request
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from joblib import load
import sklearn
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('omw-1.4')
# nltk.download('wordnet')

def check_file_type(file):
    file_extension = Path(file.filename).suffix.lower()
    if file_extension == '.eml' or file_extension == '.txt':
        save_file(file)
        return 'Extracted Features'
        # return get_features('email files/' + file.filename)
    else:
        return "Please select .eml or .txt file."

def save_file(file):
    file_path = 'email files/' + file.filename
    with open(file_path, 'w') as f:
        f.write(file.read().decode('utf-8'))

def text_feature(filepath):
    text = get_text(filepath)
    # print(text)
    if text != "":
        text = text.split()
        textlist = ' '.join(text)
        dataf = pd.DataFrame([[textlist]], columns=['text'])
        return dataf

def html_tags_feature(filepath):
    tags = get_tags_from_html(get_html_general(filepath))
    taglist = ' '.join(tags) if tags !=[] else []
    dataf = pd.DataFrame([[taglist]], columns=['tags'])
    return dataf

def extra_feature(filepath):
    spf = check_spf(filepath)
    dkim = check_dkim(filepath)
    dmarc = check_dmarc(filepath)
    deliver_receiver = check_deliver_receiver(filepath)
    encript = check_encript(filepath)
    onclick = get_onclicks(filepath)
    popwindow = check_popWindow(filepath)
    extra_data_row = [spf, dkim, dmarc, deliver_receiver, encript, onclick, popwindow]
    extra_data_row = [0 if x is None else x for x in extra_data_row]
    extra_data_row = [1 if x is True else x for x in extra_data_row]
    extra_data_row = [0 if x is False else x for x in extra_data_row]
    extra_data = pd.DataFrame([extra_data_row],
                              columns=['SPF(Pass:1,Neutral:2,Softdail:3,None:0)', 'DKIM', 'DMARC', 'Deliver-to Matches Receiver', 'Message_encrtpted', 'Onclick_events', 'Popwindow'])
    return extra_data

def num_feature(filepath):
    body_richness = get_body_richness(filepath)
    func_words = get_num_FunctionWords(filepath)
    sbj_richness = get_sbj_richness(filepath)
    urls = get_num_urls(filepath)
    ipurls = get_num_urls_ip(filepath)
    imageurls = get_num_image_urls(filepath)
    domainurls = get_num_domain_urls(filepath)
    urlport = get_num_url_ports(filepath)
    sen_chars = get_chars_sender(filepath)
    num_data_row = [body_richness, func_words, sbj_richness, urls, ipurls, imageurls, domainurls, urlport, sen_chars]
    num_data_row = [0 if x is None else x for x in num_data_row]
    num_data = pd.DataFrame([num_data_row],
                            columns=['body richness', 'Include function words', 'Subject richness', 'Numers of URLs', 'IPURLs', 'ImageURLs',
                                     'DomainURLs', 'URLs contain port information', 'Characters in senders'])
    return num_data
def get_features(filepath):
    # text
    textlist = text_feature(filepath)
    # html tags
    taglist = html_tags_feature(filepath)
    #extra feature
    extra_data = extra_feature(filepath)
    # Numeric data

    num_data = num_feature(filepath)
    combined_df = pd.concat([textlist, taglist, num_data,extra_data], axis=1)
    # print(combined_df)
    return combined_df


def predict_content(content):
    content_clf = load("save_models/SVM_finalcontent.pkl")
    predict = content_clf.predict(preprocess_content(content))
    return "Legitimate" if predict[0]=='ham' else "Phishing"

def predict_html(html_tag):
    html_clf = load("save_models/Stack_tag.pkl")
    predict = html_clf.predict(preprocess_html(html_tag))
    return "Legitimate" if predict[0]=='ham' else "Phishing"

def predict_num(num_df):
    num_clf = load("save_models/RF_Num.pkl")
    predict = num_clf.predict(preprocess_num(num_df))
    return "Legitimate" if predict[0]=='ham' else "Phishing"

def predict_extra(extra_df):
    extra_clf = load("save_models/RF_extra.pkl")
    predict = extra_clf.predict(preprocess_extra(extra_df))
    return "Legitimate" if predict[0]=='ham' else "Phishing"

def preprocess_content(content):
    with open('vectorizer/content_tfidf.pickle', 'rb') as f:
        tfidf = pickle.load(f)
    # Transform feature input to TF-IDF
    content_tfidf = tfidf.transform(content)
    return content_tfidf

def preprocess_html(html_tag):
    with open('vectorizer/html_cv.pickle', 'rb') as f:
        cv = pickle.load(f)
    tag_data = cv.transform(html_tag)
    return tag_data

def preprocess_num(num_df):
    with open('vectorizer/num_scaler.pkl', 'rb') as f:
        num_scaler = pickle.load(f)
    scale_num = num_scaler.transform(num_df.values)
    return scale_num

def preprocess_extra(extra_df):
    with open('vectorizer/extra_scaler.pkl', 'rb') as f:
        extra_scaler = pickle.load(f)
    scale_extra = extra_scaler.transform(extra_df.values)
    return scale_extra


lemmatizer = WordNetLemmatizer()
def customtokenize(str):
    # Split string as tokens
    tokens = nltk.word_tokenize(str)
    # Filter for stopwords
    nostop = list(filter(lambda token: token not in stopwords.words('english'), tokens))
    # Perform lemmatization
    lemmatized = [lemmatizer.lemmatize(word) for word in nostop]
    return lemmatized