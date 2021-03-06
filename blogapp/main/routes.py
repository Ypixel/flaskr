from blogapp import db
from blogapp.main import bp
from flask import render_template,flash,redirect,url_for,request,current_app,g
from blogapp.main.forms import EditProfileForm,PostForm,SearchForm
from blogapp.models import User,Post
from flask_login import login_user,logout_user,current_user,login_required
from werkzeug.urls import url_parse
from datetime import datetime


@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.search_form = SearchForm()


@bp.route('/',methods=['GET','POST'])
@bp.route('/index',methods=['GET','POST'])
# @login_required
def index():
	page = request.args.get('page',1,type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,current_app.config['POST_PER_PAGE'],False)
	next_url = url_for('main.index',page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.index',page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html',posts=posts.items,next_url=next_url,prev_url=prev_url)


@bp.route('/addpost',methods=['GET','POST'])
@login_required
def addpost():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data,body=form.body.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live')
		return redirect(url_for('main.index'))
	return render_template('addpost.html',form=form,title='Addpost')


@bp.route('/user/<username>')
# @login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page',1,type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(page,current_app.config['POST_PER_PAGE'],False)
	next_url = url_for('main.user',username=user.username,page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.user',username=user.username,page=posts.prev_num) if posts.has_prev else None
	return render_template('user.html',user=user,posts=posts.items,next_url=next_url,prev_url=prev_url)


@bp.route('/articles/<article_id>')
def article_details(article_id):
	post = Post.query.filter_by(id=article_id).first()
	db.session.commit()
	return render_template('article_details.html',post=post)




@bp.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit() 
		flash('Your changes have been saved.')
		return redirect(url_for('main.index'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html',title='Edit Profile',form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))

@bp.route('/search')
# @login_required
def search():
	if not g.search_form.validate():
		return redirect(url_for('main.explore'))
	page = request.args.get('page',1,type=int)
	posts,total = Post.search(g.search_form.q.data,page,current_app.config['POST_PER_PAGE'])
	next_url = url_for('main.search',q=g.search_form.q.data,page=page + 1) if total > page * current_app.config['POST_PER_PAGE'] else None
	prev_url = url_for('main.user',q=g.search_form.q.data,page=page - 1) if page > 1 else None
	return render_template('search.html',title='Search',posts=posts,next_url=next_url,prev_url=prev_url)

@bp.route('/delete_post')
@login_required
def delete_post():
	try:
		post_id = request.args.get('post_id',type=int)
	except:
		flash('delete post failed')
	Post.delete(id = post_id)
	flash('delete post success')
	return redirect(url_for('main.index'))

