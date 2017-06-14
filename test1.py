# -*- coding: utf-8 -*-
from flask import Flask
from flask import request, render_template, url_for, redirect
from werkzeug import secure_filename
import os
import boto3
import datetime
import decimal

client = boto3.client('dynamodb')
UPLOAD_FOLDER = 'path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 한글


@app.route('/')
def main():
    a = 12
    response = client.scan(TableName='test')
    result = response['Items']
    return render_template('main.html', result=result)


@app.route('/view/<dynamodbid>')
def article_view(dynamodbid):
    response = client.get_item(TableName='test', Key={'id': {'S': dynamodbid}} )
    if response.get('Item'):
        result = response['Item']
        return render_template('view.html', result=result)
    else:
        return '없습니다.'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALL


@app.route('/create', methods=['GET', 'POST'])
def article_create():
    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']
        file = request.files['file']

        item = {
            'id': {'S': str(datetime.datetime.now())},
            'subject': {'S': subject},
            'content': {'S': content},
            'file': {}
        }

        response = client.put_item(
            TableName='test',
            Item=item
        )

        return redirect(url_for('main')) # 메인화면으로 이동
    else:
        return render_template('write.html') # 글쓰기 첫 화면


@app.route('/delete/<dynamodbid>')
def article_delete(dynamodbid):
    response = client.delete_item(TableName='test', Key={'id': {'S': dynamodbid}} ,
                                  )
    return str(response)
    if response.get('Item'):
        result = response['Item']
        return render_template('view.html', result=result)
    else:
        return '없습니다.'

if __name__ == '__main__':
    app.run(debug=True)
