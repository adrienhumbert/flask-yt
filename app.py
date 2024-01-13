from flask import Flask, render_template, request, redirect, url_for, session
import pytube

app = Flask(__name__)
app.secret_key = "darahemitotanimecimavoyavafenevudekozite"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        try:
            video = pytube.YouTube(youtube_url)
            session['title'] = video.title
            streams = video.streams.filter(progressive=True, file_extension='mp4')
            if streams:
                stream = streams[-1]
                stream.download(output_path='static', filename=f'{video.title}.mp4')
                return redirect(url_for('download'))
            else:
                return "No streams found"
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template('index.html')

@app.route('/download')
def download():
    return render_template('download.html', title=session['title'])

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
