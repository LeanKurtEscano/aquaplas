from flask import  Blueprint, render_template, redirect, request, url_for,session
import mysql.connector

bl = Blueprint('bl', __name__, template_folder='template')

@bl.route('/my-blog')
def display_blog():
    colab_links = [
        'https://colab.research.google.com/drive/1c1bnf6T7O3HyFp8GBpSZi5eKnoCnzrpb',
        'https://colab.research.google.com/drive/1HnohhmACO33b8r-f8k2ecBzmTEdxw5NA',
        'https://colab.research.google.com/drive/15KBjHfjqucxcOWLeaD2HOlA_iKWOUg2q',
        'https://colab.research.google.com/drive/1FkoQvld0g0lcyrF-NlunTShd_HfB6Dhs',
        'https://colab.research.google.com/drive/1A3ksC1P7Um68f4_32zDR9HMx6FbmFuFC',
        'https://colab.research.google.com/drive/1ROoRbJem7aLCSKYbEvAsskfXfvALBI2i',
        
    ]
    return render_template("blog.html",colab_links=colab_links)