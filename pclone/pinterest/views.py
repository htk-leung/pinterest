from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.urls import reverse  
from django.db import connection
from .models import Users, Pintags
from .forms import SavePinForm, RegisterUserForm
from django.utils import timezone


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterUserForm()
    
    return render(request, 'authenticate/register.html', {'form': form})


# def register_user(request):
# 	if request.method == "POST":
# 		# extract info from register form
# 		form = RegisterUserForm(request.POST)
# 		# if form.is_valid():
# 		form.save()
# 		username = form.cleaned_data['username']
# 		password = form.cleaned_data['password1']
# 		email = form.cleaned_data['email']

# 		# insert to database
# 		with connection.cursor() as cursor:
# 			cursor.execute("""
# 				INSERT INTO users (username, email) VALUES
# 				(%s, %s);
# 			""", [username, email])

# 		# login
# 		user = authenticate(username=username, password=password)
# 		login(request, user)
# 		return redirect('home')
# 	else: 
# 		form = RegisterUserForm()
# 		return render(request, 'authenticate/register.html', {
# 			'form': form,
# 	})

def login_user(request):
	next_url = request.GET.get('next', '') or reverse('myaccount')

	if request.method == "POST":
		# extract info from login form
		username = request.POST['username'] 
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect(next_url)
		else:
			#otherwise stay on login page
			return render(request, 'authenticate/login.html', {})

	else: 
		return render(request, 'authenticate/login.html', {})
    
def logout_user(request):
	logout(request)
	return redirect('home')

def home(request):	

	search_term = 0
	category = 0
	
	if request.method == "POST" :
		# get search parameters
		search_term = request.POST.get('search-input', '')
		category = request.POST.get('category', '')

		if category == "All pins" or "Everything":
			with connection.cursor() as cursor:
				# get all pins with tags containing search_term
				cursor.execute("""
					WITH T1 (pinid) AS
						(SELECT distinct pinid FROM pintags WHERE %s LIKE tag)
					SELECT P1.pinid, U.uid, U.username, P2.pic 
					FROM T1 JOIN pins P1 ON T1.pinid = P1.pinid 
						JOIN pictures P2 ON P1.picid = P2.picid
						JOIN boards B ON P1.bid = B.bid
						JOIN users U ON B.uid = U.uid
				""", [search_term])
				pins = cursor.fetchall()

		elif category == "Your streams" :
			username = request.user.username

			with connection.cursor() as cursor:
				# get uid
				cursor.execute("""
					SELECT uid FROM users WHERE username = %s
				""", [username])
				uid = cursor.fetchone()
				# get matching pins inside your stream
				cursor.execute("""
					(SELECT distinct pinid 
					FROM (SELECT * FROM streams S WHERE uid = %s)
						JOIN streamboards SB ON S.bid = SB.bid
						JOIN pins P1 ON SB.bid = P.bid
					) 
					INTERSECT
					(SELECT distinct pinid FROM pintags WHERE %s LIKE tag)
				""", [uid[0], search_term])
				pins = cursor.fetchall()
	else:
		with connection.cursor() as cursor:
			# get all pins
			cursor.execute("""
				SELECT P1.pinid, U.uid, U.username, P2.pic 
				FROM pins P1 JOIN pictures P2 ON P1.picid = P2.picid
					JOIN boards B ON P1.bid = B.bid
					JOIN users U ON B.uid = U.uid
			""")
			pins = cursor.fetchall()	

	# pass all pins into rendered page for display
	return render(request, 'allpins.html', {
		'pins': pins,
		'search_term': search_term,
		'category' : category,
	})

@login_required(login_url = 'login_user')
def allpins(request):	
	username = request.user.username

	with connection.cursor() as cursor:
		# get uid
		cursor.execute("""
			SELECT uid
			FROM users
			WHERE username = %s
		""", [username])
		uid = cursor.fetchone()

		# get your pins
		cursor.execute("""
			SELECT P1.pinid, U.uid, U.username, P2.pic 
			FROM pins P1 JOIN pictures P2 ON P1.picid = P2.picid
				JOIN boards B ON P1.bid = B.bid
				JOIN users U ON B.uid = U.uid
			WHERE U.uid = %s
		""", [uid[0]])
		pins1 = cursor.fetchall()	

		# get liked pins
		cursor.execute("""
			SELECT P1.pinid, U.uid, U.username, P2.pic 
			FROM (SELECT pinid FROM likes WHERE uid = %s) AS L
				JOIN pins P1 ON P1.pinid = L.pinid
				JOIN pictures P2 ON P1.picid = P2.picid
				JOIN boards B ON P1.bid = B.bid
				JOIN users U ON B.uid = U.uid
		""", [uid[0]])
		pins2 = cursor.fetchall()	

		pins = pins1 + pins2

	# pass all into rendered page for display
	return render(request, 'allpins.html', {
		'pins': pins,
	})


def streampins(request, stream_id):	
	username = request.user.username

	with connection.cursor() as cursor:
		# get uid
		cursor.execute("""
			SELECT uid
			FROM users
			WHERE username = %s
		""", [username])
		uid = cursor.fetchone()
		# get all pins
		cursor.execute("""
			SELECT P1.pinid, U.uid, U.username, P2.pic 
			FROM (SELECT bid FROM streamboards WHERE sid = %s) as SB
				JOIN boards B ON SB.bid = B.bid
				JOIN users U ON B.uid = U.uid
				JOIN pins P1 ON P1.bid = B.bid
				JOIN pictures P2 ON P1.picid = P2.picid
		""", [stream_id])
		pins = cursor.fetchall()	

	# pass all into rendered page for display
	return render(request, 'allpins.html', {
		'pins': pins,
	})
	return render(request, 'streampins.html', {})


def boardpins(request, board_id):	
	username = request.user.username

	with connection.cursor() as cursor:
		# get uid
		cursor.execute("""
			SELECT U.uid
			FROM users U
			WHERE username = %s
		""", [username])
		uid = cursor.fetchone()
		# get all pins
		cursor.execute("""
			SELECT P1.pinid, U.uid, U.username, P2.pic 
			FROM (SELECT bid, uid FROM boards WHERE bid = %s) as B
				JOIN users U ON B.uid = U.uid
				JOIN pins P1 ON P1.bid = B.bid
				JOIN pictures P2 ON P1.picid = P2.picid
		""", [board_id])
		pins = cursor.fetchall()		
	# pass all into rendered page for display
	return render(request, 'allpins.html', {
		'pins': pins,
	})


def onepin(request, pinid):
	username = request.user.username

	if request.method == "POST":

		pinid = request.POST['pinid'] 
		comment = request.POST['comment']

		with connection.cursor() as cursor:
			# get uid
			cursor.execute("""
				SELECT uid
				FROM users
				WHERE username = %s
			""", [username])
			uid = cursor.fetchone()
			
			# Save comment to database
			cursor.execute("""
				INSERT INTO comments (pinid, uid, comment)
				VALUES (%s, %s, %s)
			""", [pinid, uid[0], comment])
	
	with connection.cursor() as cursor:
		# get uid
		cursor.execute("""
			SELECT U.uid
			FROM users U
			WHERE username = %s
		""", [username])
		uid = cursor.fetchone()

		# picurl
		cursor.execute("""
			SELECT P2.pic 
			FROM pins P1 JOIN pictures P2 ON P1.picid = P2.picid
			WHERE P1.pinid = %s
		""", [pinid])
		picurl = cursor.fetchone()

		# ownerinfo
		cursor.execute("""
			SELECT U.uid, U.username
			FROM pins P JOIN boards B ON P.bid = B.bid
				JOIN users U ON B.uid = U.uid
			WHERE P.pinid = %s
		""", [pinid])
		owner = cursor.fetchone()

		# boardinfo
		cursor.execute("""
			SELECT B.bid, B.bname 
			FROM pins P JOIN boards B ON P.bid = B.bid
			WHERE P.pinid = %s
		""", [pinid])
		board = cursor.fetchone()

		# comment setting
		cursor.execute("""
			SELECT B.frdonly
			FROM pins P JOIN boards B ON P.bid = B.bid
			WHERE P.pinid = %s
		""", [pinid])
		comperm = cursor.fetchone()

		# comment pinid uid
		cursor.execute("""
			SELECT U.uid, U.username, C.comment 
			FROM comments C JOIN users U ON C.uid = U.uid
			WHERE C.pinid = %s
			ORDER BY C.regtime DESC
		""", [pinid])
		comments = cursor.fetchall()

		cancomment = 1
		if comperm[0] == True and owner[0] != uid[0]:
			# friend status
			cursor.execute("""
				SELECT 1 FROM friends WHERE uid1 = %s AND uid2 = %s
			""", [uid[0], owner[0]])
			arefrds = cursor.fetchone()

			if arefrds is None:
				cancomment = 0

	return render(request, 'onepin.html', {
		'picurl': picurl,
		'pin': pinid,
		'owner': owner,
		'comments': comments,
		'cancomment': cancomment,
		'board': board,
	})


@login_required(login_url = 'login_user')
def myaccount(request):	
	if request.user.is_authenticated:
		username = request.user.username

		with connection.cursor() as cursor:
			# get uid
			cursor.execute("""
				SELECT uid FROM users WHERE username = %s
			""", [username])
			uid = cursor.fetchone()

			# get self description
			cursor.execute("""
				SELECT intro FROM users WHERE username = %s
			""", [username])
			intro = cursor.fetchone()

			# get list of boards, latest image of each
			cursor.execute("""
				SELECT B.bid, B.bname, (
						SELECT P2.pic
						FROM pins P1 JOIN pictures P2 ON P1.picid = P2.picid
						WHERE P1.bid = B.bid
						ORDER BY P1.regtime DESC
						LIMIT 1) AS pic
				FROM boards B
				WHERE B.uid = %s
			""", [uid[0]])
			boards = cursor.fetchall()

			# get list of streams
			cursor.execute("""
				SELECT S.sid, S.sname, (
						SELECT P2.pic
						FROM streamboards SB 
							JOIN pins P1 ON SB.bid = P1.bid
							JOIN pictures P2 ON P1.picid = P2.picid
						WHERE SB.sid = S.sid
						ORDER BY P1.regtime DESC
						LIMIT 1) AS pic
				FROM streams S
				WHERE S.uid = %s
			""", [uid[0]])
			streams = cursor.fetchall()

			# get list of friends and 1 of their photo
			cursor.execute("""
				SELECT F.uid2, U.username, (
						SELECT P2.pic
						FROM boards B 
							JOIN pins P1 ON B.bid = P1.bid
							JOIN pictures P2 ON P1.picid = P2.picid
						WHERE B.uid = F.uid2
						ORDER BY P1.regtime DESC
						LIMIT 1) AS pic
				FROM friends F JOIN users U ON F.uid2 = U.uid
				WHERE F.uid1 = %s
			""", [uid[0]])
			friends = cursor.fetchall()
			
	# pass all into rendered page for display
	return render(request, 'myaccount.html', {
		'username': username,
		'intro': intro,
		'boards': boards,
		'streams': streams,
		'friends': friends,
	})

def uaccount(request, uid):	
	with connection.cursor() as cursor:
		# get self description
		cursor.execute("""
			SELECT uid, username, intro FROM users WHERE uid = %s
		""", [uid])
		user = cursor.fetchone()

		# get list of boards, latest image of each
		cursor.execute("""
			SELECT B.bid, B.bname, (
					SELECT P2.pic
					FROM pins P1 JOIN pictures P2 ON P1.picid = P2.picid
					WHERE P1.bid = B.bid
					ORDER BY P1.regtime DESC
					LIMIT 1) AS pic
			FROM boards B
			WHERE B.uid = %s
		""", [uid])
		boards = cursor.fetchall()

		# get list of streams
		cursor.execute("""
			SELECT S.sid, S.sname, (
					SELECT P2.pic
					FROM streamboards SB 
						JOIN pins P1 ON SB.bid = P1.bid
						JOIN pictures P2 ON P1.picid = P2.picid
					WHERE SB.sid = S.sid
					ORDER BY P1.regtime DESC
					LIMIT 1) AS pic
			FROM streams S
			WHERE S.uid = %s
		""", [uid])
		streams = cursor.fetchall()
	# pass all into rendered page for display
	return render(request, 'uaccount.html', {
		'user': user,
		'boards': boards,
		'streams': streams,
	})


@login_required(login_url = 'login_user')
def newboard(request):
	if request.method == "POST":
		bname = request.POST['bname']
		req = request.POST['req'] 
		username = request.user.username

		with connection.cursor() as cursor:
			# get uid
			cursor.execute("""
				SELECT uid FROM users WHERE username = %s
			""", [username])
			uid = cursor.fetchone()

			if req == "Everyone":
				cursor.execute("""
					INSERT INTO boards (uid, bname, frdonly) VALUES (%s, %s, False)
				""", [uid[0], bname])

			elif req == "Friends":
				cursor.execute("""
					INSERT INTO boards (uid, bname, frdonly) VALUES (%s, %s, True)
				""", [uid[0], bname])

		return redirect('myaccount')

	else:
		return render(request, 'newboard.html', {})

@login_required(login_url = 'login_user')
def newstream(request):	
	if request.method == "POST":
		sname = request.POST['sname']
		username = request.user.username

		with connection.cursor() as cursor:
			cursor.execute("""
				SELECT uid FROM users WHERE username = %s
			""", [username])
			uid = cursor.fetchone()

			cursor.execute("""
				INSERT INTO streams (uid, sname) VALUES (%s, %s)
			""", [uid[0], sname])
		return redirect('myaccount')
	else:
		return render(request, 'newstream.html', {})

# def boardstreamfollow(request):	
# 	return render(request, 'boardstreamfollow.html', {})


@login_required(login_url = 'login_user')
def saveboardtostream(request):	
	username = request.user.username

	# after clicking save
	if 'request' in request.POST:

		bid = request.POST.get('bid')

		with connection.cursor() as cursor:
			# get uid
			cursor.execute("""
				SELECT uid FROM users WHERE username = %s
			""", [username])
			uid = cursor.fetchone()

			cursor.execute("""
				SELECT sid, sname FROM streams WHERE uid = %s
			""", [uid[0]])
			streams = cursor.fetchall()

		return render(request, 'saveboardtostream.html', {
			'streams': streams,
			'bid': bid,
		})

	elif 'savetostream' in request.POST:
		bid = request.POST['bid']
		sid = request.POST['sid']

		with connection.cursor() as cursor:
			cursor.execute("""
				INSERT INTO streamboards (sid, bid) VALUES (%s, %s)
			""", [sid, bid])
		return redirect('myaccount')
		
	# landing
	else:
		return render(request, 'saveboardtostream.html', {
			'streams': 'NONE',
			'bid': 'NONE',
		})


@login_required(login_url = 'login_user')
def savepintoboard(request, pinid):	
	username = request.user.username

	# after clicking save
	if request.method == "GET":

		with connection.cursor() as cursor:
			# get uid
			cursor.execute("""
				SELECT uid FROM users WHERE username = %s
			""", [username])
			uid = cursor.fetchone()
			# get boards
			cursor.execute("""
				SELECT bid, bname FROM boards WHERE uid = %s
			""", [uid[0]])
			boards = cursor.fetchall()
			# get picid
			cursor.execute("""
				SELECT picid FROM pins WHERE pinid = %s
			""", [pinid])
			picid = cursor.fetchone()

		return render(request, 'savepintoboard.html', {
			'picid': picid,
			'boards': boards,
		})
		
	# after saving
	else:
		bid = request.POST.get('bid').strip("'")

		picid = request.POST.get('picid').strip("'")


		with connection.cursor() as cursor:
			cursor.execute("""
				INSERT INTO pins (picid, bid, original) VALUES (%s, %s, False)
			""", [picid, bid])

		return redirect('myaccount')


@login_required(login_url = 'login_user')
def addfriend(request, uid):	
	myuname = request.user.username

	with connection.cursor() as cursor:
		# get uid
		cursor.execute("""
			SELECT uid FROM users WHERE username = %s
		""", [myuname])
		myuid = cursor.fetchone()

		cursor.execute("""
			SELECT 1 FROM friends WHERE uid1 = %s AND uid2 = %s
		""", [myuid[0], uid])
		existfriend = cursor.fetchone() is not None

		if not existfriend: # save to invitation
			cursor.execute("""
				INSERT INTO invitations (uidfr, uidto) VALUES (%s, %s)
			""", [myuid[0], uid])

	return redirect(request.META.get('HTTP_REFERER', reverse('myaccount')))


@login_required(login_url = 'login_user')
def likepin(request, pinid):	
	username = request.user.username

	with connection.cursor() as cursor:
		# get uid
		cursor.execute("""
			SELECT uid FROM users WHERE username = %s
		""", [username])
		uid = cursor.fetchone()

		cursor.execute("""
			SELECT 1 FROM likes WHERE uid = %s AND pinid = %s
		""", [uid[0], pinid])
		existlike = cursor.fetchone() is not None

	# return render(request, 'test.html', {
	# 	'uid': uid,
	# })

		if not existlike: # save to likes
			cursor.execute("""
				INSERT INTO likes (uid, pinid) VALUES (%s, %s)
			""", [uid[0], pinid])
		else: #remove from likes
			cursor.execute("""
				DELETE FROM likes WHERE uid = %s AND pinid = %s
			""", [uid[0], pinid])

	return redirect(request.META.get('HTTP_REFERER', reverse('allpins')))

@login_required(login_url = 'login_user')
def newpin(request):	
	username = request.user.username
	# after hitting save
	if request.method == "POST" :
		imageform = SavePinForm(request.POST, request.FILES)

		if imageform.is_valid():
			#save image
			imageform.save()
			#get other info
			tags = [request.POST.get(f'tag{i}') for i in range(5)]
			tags = [tag.strip() for tag in tags if tag and tag.strip()]
			bid = request.POST['bid']

			with connection.cursor() as cursor:
				# get uid
				cursor.execute("""
					SELECT uid FROM users WHERE username = %s
				""", [username])
				uid = cursor.fetchone()
				#get latest picid
				cursor.execute("""
					SELECT picid FROM pictures WHERE regtime = (
					SELECT max(regtime) FROM pictures)
				""")
				picid = cursor.fetchone()

				# insert pin
				cursor.execute("""
					INSERT INTO pins (picid, bid, original) VALUES (%s, %s, True)
				""", [picid[0], bid])

				cursor.execute("""
					SELECT pinid FROM pins WHERE regtime = (
					SELECT max(regtime) FROM pins)
				""")
				pinid = cursor.fetchone()

				# insert each tag 
				# for tag in tags:
				# 	if tag:
				# 		cursor.execute("""
				# 			INSERT INTO pintags (pinid, tag) VALUES (%s, %s)
				# 		""", [pinid[0], tag])

			return redirect('myaccount')

		return render(request, 'newpin.html', {})
	# landing, getting input boxes for tags, dropdown for boards, image upload btn
	else :
		with connection.cursor() as cursor:
			# get uid
			cursor.execute("""
				SELECT uid FROM users WHERE username = %s
			""", [username])
			uid = cursor.fetchone()
			# get boards
			cursor.execute("""
				SELECT bid, bname FROM boards WHERE uid = %s
			""", [uid[0]])
			boards = cursor.fetchall()
		# get form
		form = SavePinForm()

		return render(request, 'newpin.html', {
			'boards': boards,
			'form': form,
		})



def settings(request):	
	if request.user.is_authenticated:
		user = request.user

	with connection.cursor() as cursor:
		cursor.execute("""
			SELECT uid FROM users WHERE username = %s
		""", [user.username])
		myuid = cursor.fetchone()

	if request.method == "POST":
		# change password
		if 'password' in request.POST:
			pw = request.POST['password'] 
			# with connection.cursor() as cursor:
			# 	cursor.execute(
			# 		"UPDATE Users SET password = %s WHERE username = %s", 
			# 		[pw, user.username])

			user.set_password(pw)
			user.save()

		# change intro
		elif 'intro' in request.POST:
			intro = request.POST['intro'] 

			with connection.cursor() as cursor:
				cursor.execute(
					"UPDATE users SET intro = %s WHERE username = %s", 
					[intro, user.username])

		# friend request
		elif 'response' in request.POST:
			response = request.POST['response'] 
			uidfr = request.POST['uidfr'] 

			with connection.cursor() as cursor:
				if response == "accept":
					# update invitations
					cursor.execute("""
						UPDATE invitations 
						SET status = 1 
						WHERE uidfr = %s AND uidto = %s
					""", [uidfr, myuid[0]])
					# update friends 
					cursor.execute("""
						INSERT INTO friends (uid1, uid2) VALUES (%s, %s)
					""", [myuid[0], uidfr])
					cursor.execute("""
						INSERT INTO friends (uid1, uid2) VALUES (%s, %s)
					""", [uidfr, myuid[0]])

				elif response == "reject":
					cursor.execute("""
						UPDATE invitations 
						SET status = 2 
						WHERE uidfr = %s AND uidto = %s
					""", [uidfr, myuid[0]])

		# change comment option
		else:
			return render(request, 'settings.html', {})

		return render(request, 'settings.html', {})

	else:
		# find 2 pending invitations
		with connection.cursor() as cursor:
			cursor.execute("""
				SELECT U.username, U.uid
				FROM invitations I JOIN users U ON I.uidfr = U.uid
				WHERE uidto = %s AND status = 0
				LIMIT 2
			""", [myuid[0]])
			requests = cursor.fetchall()

		return render(request, 'settings.html', {
			'requests': requests,
		})