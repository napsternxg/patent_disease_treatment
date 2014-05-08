import logging
from logging import StreamHandler
from flask import Flask, render_template, request,redirect,url_for
from explorer import ExploreCSV
import sqlalchemy
import sys
app = Flask(__name__)
logger = StreamHandler()
logger.setLevel(logging.DEBUG)
app.logger.addHandler(logger)

@app.route("/")
def hello():
   return render_template("home.html")

@app.route('/crf_tag',methods=['GET','POST'])
def crf_tag():
  # show the user profile for that user
  #return 'User %s, Page %s' % (username,post_id)
  from crf_tag_helper import get_all_data,put_all_data, get_list,\
      get_form_list, get_list_as_array
  username = request.args.get('username', '')
  post_id = int(request.args.get('page', ''))
  if request.method == 'POST':
    print >> sys.stderr, "*"*50
    f = request.form
    """
    for key in f.keys():
      for value in f.getlist(key):
        print >> sys.stderr, key,":",value
    """
    grant_id = request.form.getlist('grant_id')
    grant_id = [str(x) for x in grant_id]
    print >> sys.stderr, "GRANT_IDS: ", grant_id
    title_d = get_form_list("title",f)
    abstract_d = get_form_list("abstract",f)
    title = {}
    abstract = {}
    for gid in grant_id:
      title[gid] = get_list_as_array(title_d[gid])
      abstract[gid] = get_list_as_array(abstract_d[gid])
      print >> sys.stderr, "TITLE: ", len(title[gid])
      print >> sys.stderr, "ABSTRACT: ", len(abstract[gid])
    next = int(request.form.get('next',''))
    put_all_data(username,grant_id,title,abstract)
    return redirect('/gimli/crf_tag?username={0}&page={1}'.format(username,next))
  if post_id == -1:
    return "Well Done %s. Finished Tagging." % username
  data = {}
  data['username'] = username
  N=3
  GIDS = get_list(username)
  print >> sys.stderr, post_id, GIDS[post_id:post_id+N]
  TOTAL = len(GIDS)
  data['page'] = post_id
  data['next'] = post_id + N if post_id < TOTAL  else -1
  data['items'] = get_all_data(username,GIDS[post_id:post_id+N])
  return render_template("crf_tag.html", data=data)

if __name__ == "__main__":
  app.debug = True
  app.run(debug=True)
