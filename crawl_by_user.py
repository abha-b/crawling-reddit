
# importing necessary modules
import sys
import praw
import pandas as pd
import datetime

'''
Following instructions on http://www.storybench.org/how-to-scrape-reddit-with-python/
Created reddit app at https://ssl.reddit.com/prefs/apps/
app name: xxx
description: zzz
personal use script: yyy
secret key: www
Example run: python crawl_by_user.py <file_with_user_list_sep_by_newline>
'''

convert2date = lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')

##########################################################################################

# extract submission info into a dictionary
def get_posts_dict(uname, submissions, fi_name):

	posts_dict = { "title":[], "score":[], "id":[], "url":[],\
		 "comms_num": [], "created": [], "username":[], "body":[], "subreddit":[]}
	
	try:
		for submission in submissions:
			# filtering out empty/deleted submissions or submissions posted in Alzheimers or Dementia groups
			if (submission.selftext) and (submission.selftext != '[removed]'):
				
				posts_dict["title"].append(submission.title)
				posts_dict["score"].append(submission.score)
				posts_dict["id"].append(submission.id)
				posts_dict["url"].append(submission.url)
				posts_dict["username"].append(str(submission.author))
				posts_dict["subreddit"].append(str(submission.subreddit))
				posts_dict["comms_num"].append(submission.num_comments)
				posts_dict["created"].append(convert2date(submission.created))
				posts_dict["body"].append(submission.selftext)
	except:
			fo = open(fi_name.replace('.csv', '_deleted_submissions.csv'), 'a+')
			fo.write(uname + ' submissions not available.\n')
			fo.close()
		
	return posts_dict
	
##########################################################################################

# extract submission info into a dictionary
def get_comments_dict(uname, comments, fi_name):

	comments_dict = { "id":[],"username":[], "subreddit":[], "created": [], "body":[], "link_id":[], "parent_id":[]}
	
	try:
		for comm in comments:
			# filtering out empty/deleted submissions or submissions posted in Alzheimers or Dementia groups
			if (comm.body):
				comments_dict["created"].append(convert2date(comm.created))
				comments_dict["body"].append(comm.body)
				comments_dict["username"].append(str(comm.author))
				comments_dict["subreddit"].append(str(comm.subreddit))
				comments_dict["id"].append(comm.id)
				comments_dict["link_id"].append(comm.link_id)
				comments_dict["parent_id"].append(comm.parent_id)
	
	except:
		fo = open(fi_name.replace('.csv', '_deleted_comments.csv'), 'a+')
		fo.write(uname + ' comments not available.\n')
		fo.close()
					
	return comments_dict
	
##########################################################################################

# write user submissions (posts) info onto a file
def write_u_subs(reddit, uname, m, hbool, fi_name):

	u_reddit = reddit.redditor(uname)
	
	print('getting submissions by user: ' + uname)
	u_submissions = u_reddit.submissions.top(limit=None)
	u_submissions_dict = get_posts_dict(uname, u_submissions, fi_name)
	u_submissions_data = pd.DataFrame(u_submissions_dict)
	u_submissions_data.to_csv(fi_name.replace('.csv', '_submissions.csv'), index=False, mode=m, header=hbool) 

	print('getting comments by user: ' + uname)
	u_comments = u_reddit.comments.top(limit=None)
	u_comments_dict = get_comments_dict(uname, u_comments, fi_name)
	u_comments_data = pd.DataFrame(u_comments_dict)
	u_comments_data.to_csv(fi_name.replace('.csv', '_comments.csv'), index=False, mode=m, header=hbool)

	return
	
##########################################################################################
'''
OBJECTIVE:
	to get all submissions and comments of users from a given list
	
INPUTS: 
	file name containing user list 
			  
OUTPUT: 
	file containing all submissions and comments by users in the list
'''
##########################################################################################

def main(fi_name):
		 
	# create reddit object instance
	reddit = praw.Reddit(client_id=<client_id>, \
		client_secret=<secret_key>, \
		user_agent=<app_name>, username=<user_name>, \
		password=<pwd>)
	
	fi = open(fi_name, 'r')
	fi.readline()
	list_users = [line.strip() for line in fi]
	list_users = [u for u in list_users if len(u)>0]
	fi.close()
	
	# for users in the list
	
	write_u_subs(reddit, list_users[0], 'a+', True, fi_name)
	for u in list_users[1:]:
		write_u_subs(reddit, u, 'a+', False, fi_name)
	
	print('Done.')
	
	return

##########################################################################################
	
# call the main function
main(sys.argv[1])

##########################################################################################