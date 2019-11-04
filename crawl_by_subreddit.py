
# importing necessary modules
import sys
import praw
import pandas as pd
import datetime as dt

'''
Following instructions on http://www.storybench.org/how-to-scrape-reddit-with-python/
Created reddit app at https://ssl.reddit.com/prefs/apps/
app name: xxx
description: zzz
personal use script: yyy
secret key: www
Example run: python crawl_by_subreddit.py <subreddit_name>
'''

##########################################################################################

# extract submission info into a dictionary
def get_posts_dict(submissions, cond):

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
				posts_dict["created"].append(submission.created)
				posts_dict["body"].append(submission.selftext)
	except:
		try:
			fo = open(cond + '_deleted_posts.csv', 'a+')
			fo.write('\t'.join([str(submission.subreddit), str(submission.author), submission.id]) + '\n')
			fo.close()
		except:
			fo = open(cond + '_deleted_posts.csv', 'a+')
			fo.write('subreddit ' + str(submission.subreddit) + '/' + str(submission.author) + ' posts not available')
			fo.close()
		
	return posts_dict
	
##########################################################################################

# extract submission info into a dictionary
def get_comments_dict(comments, cond):

	comments_dict = { "id":[],"username":[], "subreddit":[], "created": [], "body":[], "link_id":[], "parent_id":[]}
	
	try:
		for comm in comments:
			# filtering out empty/deleted submissions or submissions posted in Alzheimers or Dementia groups
			if (comm.body):
				comments_dict["created"].append(comm.created)
				comments_dict["body"].append(comm.body)
				comments_dict["username"].append(str(comm.author))
				comments_dict["subreddit"].append(str(comm.subreddit))
				comments_dict["id"].append(comm.id)
				comments_dict["link_id"].append(comm.link_id)
				comments_dict["parent_id"].append(comm.parent_id)
				#print(comments_dict)
	
	except:
		try:
			fo = open(cond + '_deleted_comments.csv', 'a+')
			fo.write('\t'.join(map(str, [str(comm.subreddit), str(comm.author), comm.id])) + '\n')
			fo.close()
		except:
			fo = open(cond + '_deleted_comments.csv', 'a+')
			fo.write('subreddit ' + str(comm.subreddit) + '/' + str(comm.author) + ' comments not available')
			fo.close()
					
	return comments_dict
	
##########################################################################################

# write user submissions (posts) info onto a file
def write_u_subs(reddit, uname, m, hbool, cond):

	u_reddit = reddit.redditor(uname)
	
	print('getting submissions by user: ' + uname)
	u_submissions = u_reddit.submissions.top(limit=None)
	u_submissions_dict = get_posts_dict(u_submissions, cond)
	u_submissions_data = pd.DataFrame(u_submissions_dict)
	u_submissions_data.to_csv('control_posts_' + cond + '.csv', index=False, mode=m, header=hbool) 

	print('getting comments by user: ' + uname)
	u_comments = u_reddit.comments.top(limit=None)
	u_comments_dict = get_comments_dict(u_comments, cond)
	u_comments_data = pd.DataFrame(u_comments_dict)
	u_comments_data.to_csv('control_comments_' + cond + '.csv', index=False, mode=m, header=hbool)

	return
	
##########################################################################################
'''
OBJECTIVE:
	to get all posts of users posting in the target subreddit 
	
INPUT: 
	subreddit name
			  
OUTPUT: 
	files containing all submissions and comments by users posting in the given subreddit
'''
##########################################################################################

def main(cond):
		 
	# create reddit object instance
	reddit = praw.Reddit(client_id=<client_id>, \
		client_secret=<secret_key>, \
		user_agent=<app_name>, username=<user_name>, \
		password=<pwd>)
		
	subreddit = reddit.subreddit(cond)
	
	print('\ngetting submissions for subreddit: ' + cond)
	# for the given subreddit, extract all posts, convert to dataframe and print onto output files
	s_submissions = subreddit.top(limit=None)
	s_submissions_dict = get_posts_dict(s_submissions, cond)
	s_submissions_data = pd.DataFrame(s_submissions_dict)
	s_submissions_data.to_csv('posts_' + cond + '.csv', index=False) 
	print('*'*50 + '\n')
	users_submissions = list(set(s_submissions_data.username))
	print(len(users_submissions))

	print('\ngetting comments for subreddit: ' + cond)	
	# for the given subreddit, extract all comments, convert to dataframe and print onto output files
	s_comments = subreddit.comments(limit=None)
	s_comments_dict = get_comments_dict(s_comments, cond)
	s_comments_data = pd.DataFrame(s_comments_dict)
	s_comments_data.to_csv('comments_' + cond + '.csv', index=False) 
	print('*'*50 + '\n')
	users_comments = list(set(s_comments_data.username))
	print(len(users_comments))
	
	print('Done.')
	
	return

##########################################################################################
	
# call the main function
main(sys.argv[1])

##########################################################################################