#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

# データベースファイルのパスを設定
dbname = '0520.db'

# テーブルの作成
con = sqlite3.connect(dbname)
cur = con.cursor()
create_table = 'create table if not exists aoz (num int, title varchar(256), author varchar(256))'
cur.execute(create_table)
con.commit()
create_tab = 'create table if not exists kekka (num int, title varchar(256), author varchar(256))'
cur.execute(create_tab)
con.commit()
cur.close()
con.close()

def application(environ,start_response):
    # HTML（共通ヘッダ部分）とCSS
    html = '<html lang="ja">\n' \
           '<head>\n' \
           '<meta charset="UTF-8">\n' \
           '<title>課題6</title>\n' \
           '<link rel="stylesheet" href="default.css">\n' \
           '<style type="text/css">\n' \
           '<!--\n' \
           'h1 {\n' \
           'width: 300px;\n' \
           'padding:40px;\n' \
           'text-align: center;\n' \
           '}\n' \
           '.box {\n' \
           'border-radius: 10px;\n' \
           'box-shadow: 3px 3px 3px gray;\n' \
           'border-bottom: solid 3px gray;\n' \
           'background-color: white;\n' \
           'font-size: 11px;\n' \
           'text-align: center;\n' \
           'transition: 0.2s;\n' \
           '}\n' \
           '.box:hover {\n' \
           'background-color: yellow;\n' \
           'font-size: 11px;\n' \
           'border-radius: 10px;\n' \
            '}\n' \
           '.box:active{\n' \
           'transform: translateY(2px);\n' \
           '}\n' \
           '.purple {\n' \
           ' color : purple;\n' \
           '}\n' \
           '.red {\n' \
           ' color : red;\n' \
           '}\n' \
           '-->\n' \
           '</style>\n' \
           '</head>\n'
    
    # フォームデータを取得
    form = cgi.FieldStorage(environ=environ,keep_blank_values=True)
    if ('v1' not in form) or ('v2' not in form) or ('v3' not in form):
        # 入力フォームの内容が空の場合（初めてページを開いた場合も含む）
        print("a")
        # HTML（入力フォーム部分）
        html += '<body>\n' \
                '<h1>検索フォーム</h1>\n' \
                '<h2>　データベース上に<span class="red">追加</span>（項目を一つ以上埋めてください！）</h2>\n' \
                '<div class="form1">\n' \
                '<form>\n' \
                '<span class="purple">数字</span>の追加　　　　　（整数） <input type="text" name="v1"><br>\n' \
                '<span class="purple">タイトル</span>の追加　　（文字列） <input type="text" name="v2"><br>\n' \
                '<span class="purple">著者</span>の追加　　　　（文字列） <input type="text" name="v3"><br>\n' \
                '　　　　　　　　　　　　　　　　　　<input type="submit" class="box" value="追加">\n' \
                '<h2>　データベースから<span class="red">検索</span>（項目を一つだけ埋めてください！）</h2>\n' \
                '<span class="purple">タイトル</span>の検索　　（文字列） <input type="text" name="v4"><br>\n' \
                '<span class="purple">著者</span>の検索　　　　（文字列） <input type="text" name="v5"><br>\n' \
                '　　　　　　　　　　　　　　　　　　<input type="submit" class="box" value="検索">\n' \
                '<h2>　データベースから<span class="red">削除</span></h2>\n' \
                '<span class="purple">タイトル</span>の削除　　（文字列） <input type="text" name="v6"><br>\n' \
                '　　　　　　　　　　　　　　　　　　<input type="submit" class="box" value="削除">\n' \
                '</form>\n' \
                '</div>\n' \
                '</body>\n'
        
    elif (form.getvalue("v4", "0") == '') and (form.getvalue("v5", "0") == '')and (form.getvalue("v6", "0") == ''):
        # 第4,5,6入力フォームの内容が空の場合
        print("b")
        # フォームデータから各フィールド値を取得
        v1 = form.getvalue("v1", "0")
        v2 = form.getvalue("v2", "0")
        v3 = form.getvalue("v3", "0")

        # データベース接続とカーソル生成
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str

        # SQL文（insert）の作成と実行
        sql = 'insert into aoz (num, title, author) values (?,?,?)'
        cur.execute(sql, (v1,v2,v3))
        con.commit()

        # SQL文（select）の作成
        sql = 'select * from aoz'

        # SQL文の実行とその結果のHTML形式への変換
        html += '<body>\n' \
                '<h1>検索結果</h1>\n' \
                '<div class="ol1">\n' \
                '<ol>\n'
        for row in cur.execute(sql):
            html +='<li>' + str(row[0]) + ',' + row[1] + ',' + row[2] + '</li>\n'
        html += '</ol>\n' \
                '</div>\n' \
                '<a href="/">追加・検索ページに戻る</a>\n' \
                '</body>\n'

        # カーソルと接続を閉じる
        cur.close()
        con.close()

    elif  form.getvalue("v4", "0") != '':
        # 第４入力フォームの内容がある場合、タイトル検索
        print("c")
        # フォームデータから各フィールド値を取得
        v4 = form.getvalue("v4", "0")

        # データベース接続とカーソル生成
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str

        #結果データベースを全て削除
        sql = 'delete from kekka'
        cur.execute(sql)
        con.commit()

        hit = []
        sql = 'select * from aoz'
        for row in cur.execute(sql):
            if len(v4) > len(row[1]):
                #入力の文字列がデータベースの文字列より長いとき
                continue
            if v4 in row[1]:
                 #入力の文字列と同じ文字列が先頭にあるとき
                 hit.append([row[0], row[1], row[2]])
        for i in hit:
            sql = 'insert into kekka (num, title, author) values (?,?,?)'
            cur.execute(sql, (i[0],i[1],i[2]))
            con.commit()

        sql = 'select * from kekka'
        #結果をHTMLで表示
        html += '<body>\n' \
                '<div class="ol2"\n>' \
                '<ol>\n' 
        for row in cur.execute(sql):
            html +='<li>' + str(row[0]) + ',' + row[1] + ',' + row[2] + '</li></label>\n'
        html += '</ol>\n' \
                '</div>\n' \
                '<a href="/">追加・検索ページに戻る</a>\n' \
                '</body>'

        #接続を終了
        cur.close()
        con.close()
    
    elif  form.getvalue("v5", "0") != '':
        # 第5入力フォームの内容がある場合、著者検索
        print("d")
        # フォームデータから各フィールド値を取得
        v5 = form.getvalue("v5", "0")

        # データベース接続とカーソル生成
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str

        #結果データベースを全て削除
        sql = 'delete from kekka'
        cur.execute(sql)
        con.commit()

        hit = []
        sql = 'select * from aoz'
        for row in cur.execute(sql):
            if len(v5) > len(row[2]):
                #入力の文字列がデータベースの文字列より長いとき
                continue
            if v5 in row[2]:
                 #入力の文字列と同じ文字列が先頭にあるとき
                 hit.append([row[0], row[1], row[2]])
        for i in hit:
            sql = 'insert into kekka (num, title, author) values (?,?,?)'
            cur.execute(sql, (i[0],i[1],i[2]))
            con.commit()

        sql = 'select * from kekka'
        #結果をHTMLで表示
        html += '<body>\n' \
                '<div class="ol2"\n>' \
                '<ol>\n'
        for row in cur.execute(sql):
            html += '<li>' + str(row[0]) + ',' + row[1] + ',' + row[2] + '</li>\n'
        html += '</ol>\n' \
                '</div>\n' \
                '<a href="/">追加・検索ページに戻る</a>\n' \
                '</body>'

        #接続を終了
        cur.close()
        con.close()

    elif  form.getvalue("v6", "0") != '':
        # 第6入力フォームの内容がある場合、タイトル削除
        print("e")
        # フォームデータから各フィールド値を取得
        v6 = form.getvalue("v6", "0")

        # データベース接続とカーソル生成
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str

        # SQL文（insert）の作成と実行
        sql = 'delete from aoz where title= ?'
        cur.execute(sql, (v6,))
        con.commit()

        # SQL文（select）の作成
        sql = 'select * from aoz'

        # SQL文の実行とその結果のHTML形式への変換
        html += '<body>\n' \
                '<h1>検索結果</h1>\n' \
                '<div class="ol1">\n' \
                '<ol>\n'
        for row in cur.execute(sql):
            html +='<li>' + str(row[0]) + ',' + row[1] + ',' + row[2] + '</li>\n'
        html += '</ol>\n' \
                '</div>\n' \
                '<a href="/">追加・検索ページに戻る</a>\n' \
                '</body>\n'

        # カーソルと接続を閉じる
        cur.close()
        con.close()
    else:
        # データベース接続とカーソル生成
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str

        html += '<body>\n' \
                '<div class="ol3">\n' \
                '<ol>\n'
        html += '</ol>\n' \
                '</div>\n' \
                '<a href="/">追加・検索ページに戻る</a>\n' \
                '</body>\n'

        # カーソルと接続を閉じる
        cur.close()
        con.close()
        

    html += '</html>\n'
    html = html.encode('utf-8')

    # レスポンス
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html))) ])
    return [html]

# リファレンスWEBサーバを起動
#  ファイルを直接実行する（python3 kadai6.py）と，
#  リファレンスWEBサーバが起動し，http://localhost:8080 にアクセスすると
#  このサンプルの動作が確認できる．
#  コマンドライン引数にポート番号を指定（python3 kadai6.py ポート番号）した場合は，
#  http://localhost:ポート番号 にアクセスする．
from wsgiref import simple_server
if __name__ == '__main__':
    port = 8080
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    server = simple_server.make_server('', port, application)
    server.serve_forever()
