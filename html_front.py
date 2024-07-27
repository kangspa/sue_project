from flask import Flask, render_template_string, request
import pymysql

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def sue():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # 검색어를 가져옴
    query = request.form.get('q')

    # 검색어가 없을 경우, 전체 뉴스 기사를 가져옴
    if not query:
        sql = "SELECT * FROM news ORDER BY post DESC"
        cur.execute(sql)
        result = cur.fetchall()
    else:
        # 검색어를 포함하는 뉴스 기사를 가져옴
        sql = "SELECT * FROM news WHERE title LIKE %s OR summary_short LIKE %s OR summary_middle LIKE %s OR summary_long LIKE %s ORDER BY post DESC"
        cur.execute(sql, ('%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%'))

        result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE</title>

                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>

            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) </h1>


                <div style="float: left; font-size: 20px">
                    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/sbs">SBS</a>   <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs">KBS</a>    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/mbc">MBC</a>
                </div>


                <div style="text-align: right;">
                    <form method="post">
                        <input type="text" name="q" size="40" placeholder="검색어를 입력하세요">
                        <input type="submit" value="검색">
                    </form>
                </div>

                <br><br>

                
                
                <style>
                ul{
                    list-style: none;
                    }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)


@app.route('/sbs')
def sbs():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'SBS' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - SBS</title>

                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>

            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - SBS</h1>
                <div style="float: right; font-size: 20px">
                    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/">전체</a>
                </div>
                
                <div style="float: left; font-size: 20px">
                    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/sbs/정치">정치</a>   <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/sbs/경제">경제</a>    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/sbs/사회">사회</a> <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/sbs/국제">국제</a> <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/sbs/생활·문화">생활·문화</a> <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/sbs/스포츠">스포츠</a>  <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/sbs/연예">연예</a>
                </div>
                <br><br><br>


                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)

@app.route('/kbs')
def kbs():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS</title>

                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>

            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS</h1>
                
                <div style="float: right; font-size: 20px">
                    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/">전체</a>
                </div>
                
                <div style="float: left; font-size: 20px">
                    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/정치">정치</a>   <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/경제">경제</a>    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/사회">사회</a> <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/문화">문화</a> <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/IT·과학">IT·과학</a> <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/국제">국제</a>  <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/재난·환경">재난·환경</a>  <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/생활·건강">생활·건강</a>  <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/스포츠">스포츠</a>  <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/연예">연예</a>  <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/날씨">날씨</a>  <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/kbs/이슈">이슈</a>  
                </div>
                <br><br><br>


                
                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)

@app.route('/mbc')
def mbc():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'MBC' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - MBC</title>

                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>

            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - MBC</h1>
                
                <div style="float: right; font-size:20px">
                    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px"; href="/">전체</a>
                </div>

                <div style="float: left; font-size: 20px">
                    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/mbc/정치">정치</a>   <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/mbc/사회">사회</a>    <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/mbc/국제">국제</a> <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/mbc/경제">경제</a> <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/mbc/스포츠">스포츠</a> <a style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;" href="/mbc/iMBC 연예">iMBC 연예</a>
                </div>
                <br><br><br>

                
                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)

@app.route('/sbs/정치')
def sbs_1():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'SBS' and field = '정치' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - SBS / 정치</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - SBS / 정치</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/sbs">SBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
               <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)

@app.route('/sbs/경제')
def sbs_2():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'SBS' and field = '경제' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - SBS / 경제</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - SBS / 경제</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/sbs">SBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)

@app.route('/sbs/사회')
def sbs_3():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'SBS' and field = '사회' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - SBS / 사회</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - SBS / 사회</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/sbs">SBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)


@app.route('/sbs/국제')
def sbs_4():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'SBS' and field = '국제' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - SBS / 국제</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - SBS / 국제</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/sbs">SBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/sbs/생활·문화')
def sbs_5():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'SBS' and field = '생활·문화' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - SBS / 생활·문화</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - SBS / 생활·문화</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/sbs">SBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)


@app.route('/sbs/스포츠')
def sbs_6():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'SBS' and field = '스포츠' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - SBS / 스포츠</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - SBS / 스포츠</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/sbs">SBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/sbs/연예')
def sbs_7():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'SBS' and field = '연예' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - SBS / 연예</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - SBS / 연예</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/sbs">SBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/kbs/정치')
def kbs_1():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '정치' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 정치</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 정치</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)




@app.route('/kbs/경제')
def kbs_2():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '경제' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 경제</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 경제</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/kbs/사회')
def kbs_3():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '사회' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 사회</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 사회</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)




@app.route('/kbs/문화')
def kbs_4():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '문화' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 문화</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 문화</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/kbs/IT·과학')
def kbs_5():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = 'IT·과학' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / IT·과학</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / IT·과학</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/kbs/국제')
def kbs_6():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '국제' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 국제</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 국제</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)





@app.route('/kbs/재난·환경')
def kbs_7():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '재난·환경' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 재난·환경</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 재난·환경</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)




@app.route('/kbs/생활·건강')
def kbs_8():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '생활·건강' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 생활·건강</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 생활·건강</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/kbs/스포츠')
def kbs_9():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '스포츠' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 스포츠</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 스포츠</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/kbs/연예')
def kbs_10():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '연예' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 연예</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 연예</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)




@app.route('/kbs/날씨')
def kbs_11():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '날씨' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 날씨</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 날씨</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/kbs/이슈')
def kbs_12():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'KBS' and field = '이슈' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - KBS / 이슈</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - KBS / 이슈</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/kbs">KBS</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/mbc/정치')
def mbc_1():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'MBC' and field = '정치' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - MBC / 정치</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - MBC / 정치</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/mbc">MBC</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/mbc/사회')
def mbc_2():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'MBC' and field = '사회' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - MBC / 사회</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - MBC / 사회</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/mbc">MBC</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/mbc/국제')
def mbc_3():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'MBC' and field = '국제' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - MBC / 국제</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - MBC / 국제</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/mbc">MBC</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)




@app.route('/mbc/경제')
def mbc_4():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'MBC' and field = '경제' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - MBC / 경제</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - MBC / 경제</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/mbc">MBC</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)




@app.route('/mbc/스포츠')
def mbc_5():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'MBC' and field = '스포츠' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - MBC / 스포츠</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - MBC / 스포츠</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/mbc">MBC</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)



@app.route('/mbc/iMBC 연예')
def mbc_6():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='012345', db='sue', charset='utf8mb4')
    cur = conn.cursor()

    # SBS로 묶어놓은 글 불러오기
    sql = "SELECT * FROM news WHERE company = 'MBC' and field = 'iMBC 연예' ORDER BY post DESC"
    cur.execute(sql)
    result = cur.fetchall()

    conn.close()

    # HTML 코드를 직접 작성하여 렌더링
    html = """
        <html>
            <head>
                <title>SUE - MBC / iMBC 연예</title>
                <style>
                    .article-box {
                        display: flex;
                        border: 3px solid #ccc;
                        padding: 10px;
                        margin-bottom: 20px;
                        }

                    .article-container {
                        align-items: center;
                        margin-bottom: 20px;
                        }

                    .article-image {
                        margin-left: 20px;
                        }

                    .article-content {
                        flex: 1;
                        overflow-wrap: break-word;
                        }

                    .article-image img {
                        width: 500px; /* 이미지의 너비를 조절합니다 */
                        height: auto; /* 이미지의 높이를 자동으로 조절하여 가로세로 비율을 유지합니다 */
                        }

                    .article-summary {
                        margin-top: 10px;
                        font-weight: bold;
                        }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">SUE (SUM UP EVERYTHING) - MBC / iMBC 연예</h1>
                
                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/">전체</a>
                </div>

                <div style="display: inline-block; border: 1px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px; float: right;">
                    <a href="/mbc">MBC</a>
                </div>



                <style>
                ul {
                    list-style: none;
                }
                </style>
                
                <ul>
                {% for record in result %}
                <div class="article-container">
                    <div class="article-box">
                        <div class="article-content">

                            <li style="font-size: 24px;"><a href="{{ record[3] }}">{{ record[2] }}</a></li>
                            <br>
                            <li style="display: inline-block; border: 3px solid #C9C9C9; padding: 0.3em 1em;border-radius: 2px;">{{ record[0] }} || {{ record[6] }} 기자 || {{ record[5] }} || {{ record[4] }}</li>
                            <br> <br>

                            <h3>SUMMARY LENGTH:</h3>
                            <input type="radio" name="content-type-{{ loop.index }}" value="type1" checked> SHORT
                            <input type="radio" name="content-type-{{ loop.index }}" value="type2"> MIDDLE
                            <input type="radio" name="content-type-{{ loop.index }}" value="type3"> LONG

                            <br><br>
                            <li class="article-summary-{{ loop.index }}"></li>
                            <script>
                            // 기사 내용 종류별로 저장된 배열
                                var contentTypes{{ loop.index }} = {
                                    type1: {
                                        summary: "{{ record[7]|safe }}"
                                    },
                                    type2: {
                                        summary: "{{ record[8]|safe }}"
                                    },
                                    type3: {
                                        summary: "{{ record[9]|safe }}"
                                    }
                                };

                            // 기사 내용을 변경하는 함수
                            function updateContent{{ loop.index }}() {
                                var contentType = document.querySelector('input[name="content-type-{{ loop.index }}"]:checked').value;
                                var articleSummaryElement = document.querySelector('.article-summary-{{ loop.index }}');

                                // 선택한 종류의 내용으로 변경
                                articleSummaryElement.textContent = contentTypes{{ loop.index }}[contentType].summary;
                            }

                            // 종류 선택이 변경될 때마다 기사 내용 업데이트
                            var contentTypeInputs{{ loop.index }} = document.querySelectorAll('input[name="content-type-{{ loop.index }}"]');
                            Array.from(contentTypeInputs{{ loop.index }}).forEach(function (input) {
                                input.addEventListener('change', updateContent{{ loop.index }});
                            });

                            // 초기 로드 시 기사 내용 업데이트
                            updateContent{{ loop.index }}();
                            </script>

                            </div>

                            <br>

                        <div class="article-image">
                            <img src="{{ record[1] }}" alt="기사 이미지">
                        </div>
                    </div>


                    <br><br><br>
                </div>
                {% endfor %}


                </ul>
            </body>
        </html>
    """

    return render_template_string(html, result=result)





                    

if __name__ == '__main__':
    app.run()
    