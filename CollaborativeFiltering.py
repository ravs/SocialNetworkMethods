'''
Python script to predict rating for item using Collaborative Filtering [user-based and item-based]
Ravs, Fall 2013

Input:
u.data from http://grouplens.org/datasets/movielens/
User-Item Matrix
Neighborhood size
User id 'u'
Item id 'i'

Output:
Predicted rating for user based CF and item based CF
'''
#!/usr/bin/env python

import sys
import math
import operator

#---------INPUT------------
data = open("u.data", "r") # initialize with local file, just for var decl
neighborhood_size = 2 # by default keep it 2

#----------AUXILIARY DATASTRUCTURE----------
# Dict of Dict to store {user_id: {item_id1: rating, item_id2: rating, ...}}
# Dict of dict is most appropriate datastructure since we can get the feature
# vector for all the ratings for items by using user_id as key directly.
user_data = {} # for user based CF
item_data = {} # for item based CF
# Use set to store all user and item ids, set is efficient than list
user_set = set()
item_set = set()
# Store similarity value since it is used in CF formula
user_sim = {}
movie_sim = {}
# List to store the top similar neighbor
top_similar_users = []
top_similar_movies = []

# Function to calculate cosine similarity of subject
# with other users for the subjectItem movie
def similarity(subject, subjectItem):
	user_sim[subject] = {}
	for user in user_set:
		if user != subject:
			user_sim[subject][user] = 0
	for user in user_set:
		if user != subject:
			temp_sum = 0
			temp_sq_sub = 0
			temp_sq_user = 0
			for item in item_set:
				if item != subjectItem:
					temp_sum = temp_sum + user_data[subject][item]*user_data[user][item]
					temp_sq_sub = temp_sq_sub + user_data[subject][item]*user_data[subject][item]
					temp_sq_user = temp_sq_user + user_data[user][item]*user_data[user][item]
			sim = temp_sum / (math.sqrt(temp_sq_sub)*math.sqrt(temp_sq_user))
			user_sim[subject][user] = sim
			#print "Similarity (" + str(subject) + "," + str(user) + ") : " + str(user_sim[subject][user])
	#print user_sim

def similarityForMovie(subject, subjectItem):
	movie_sim[subject] = {}
	for movie in item_set:
		if movie != subject:
			movie_sim[subject][movie] = 0
	for movie in item_set:
		if movie != subject:
			temp_sum = 0
			temp_sq_sub = 0
			temp_sq_user = 0
			for user in user_set:
				if user != subjectItem:
					temp_sum = temp_sum + item_data[subject][user]*item_data[movie][user]
					temp_sq_sub = temp_sq_sub + item_data[subject][user]*item_data[subject][user]
					temp_sq_user = temp_sq_user + item_data[movie][user]*item_data[movie][user]
			sim = temp_sum / (math.sqrt(temp_sq_sub)*math.sqrt(temp_sq_user))
			movie_sim[subject][movie] = sim
			#print "Similarity (" + str(subject) + "," + str(movie) + ") : " + str(movie_sim[subject][movie])
	#print user_sim


# Function to get the top n similar neighbors of subject
# where n in neighborhood_size
def getTopSimilarNeighbor(subject, subjectItem):
	similarity(subject, subjectItem)
	sorted_similarity = sorted(user_sim[subject].items(), key = operator.itemgetter(1))
	sorted_similarity.reverse()
	print "Top " + str(neighborhood_size) + " similar neighbors of subject " + str(subject) + " are:"
	idx = 0;
	for item in sorted_similarity:
		if idx<neighborhood_size:
			print "User " + str(item[0]) + " with similarity value = " + str(item[1])
			top_similar_users.append(item[0])
			idx = idx + 1
		else:
			break

def getTopSimilarNeighborForMovie(subject, subjectItem):
	similarityForMovie(subject, subjectItem)
	sorted_similarity = sorted(movie_sim[subject].items(), key = operator.itemgetter(1))
	sorted_similarity.reverse()
	print "Top " + str(neighborhood_size) + " similar neighbors of subject " + str(subject) + " are:"
	idx = 0;
	for item in sorted_similarity:
		if idx<neighborhood_size:
			print "Movie " + str(item[0]) + " with similarity value = " + str(item[1])
			top_similar_movies.append(item[0])
			idx = idx + 1
		else:
			break

# Function to calculate average rating for users
def averageUserRating(user):
	rating = 0.0
	tempSum = 0.0
	for key in user_data[user]:
		tempSum = tempSum + user_data[user][key]
	rating = tempSum/len(user_data[user])
	print "Average rating for user " + str(user) + " = " + str(rating)
	return rating

# Function to calculate average rating for users
def averageMovieRating(movie):
	rating = 0.0
	tempSum = 0.0
	for key in item_data[movie]:
		tempSum = tempSum + item_data[movie][key]
	rating = tempSum/len(item_data[movie])
	print "Average rating for movie " + str(movie) + " = " + str(rating)
	return rating

# Function fo calculate average rating for subject
# Think for more efficient method such that both
# functions can be coupled/overloaded
# user -> refered user, movie -> refered movie
def averageRatingForUser(user, movie):
	rating = 0.0
	tempSum = 0.0
	for key in user_data[user]:
		if key != movie:
			tempSum = tempSum + user_data[user][key]
	rating = tempSum/(len(user_data[user])-1)
	print "Average rating for user " + str(user) + " = " + str(rating)
	return rating

# movie -> refered movie, user -> refered user
def averageRatingForMovie(movie, user):
	rating = 0.0
	tempSum = 0.0
	for key in item_data[movie]:
		if key != user:
			tempSum = tempSum + item_data[movie][key]
	rating = tempSum/(len(item_data[movie])-1)
	print "Average rating for movie " + str(movie) + " = " + str(rating)
	return rating


# Utility method to extract Users and items
def extractData():
	for line in data:
		temp = line.split("\t")
		if temp[0] not in user_set:
			user_set.add(int(temp[0]))
		if temp[1] not in item_set:
			item_set.add(int(temp[1]))
	#print "Set of user ids:"
	#print ",".join(str(user) for user in user_set)
	#print "Set of item ids:"
	#print ",".join(str(item) for item in item_set)

# Initialize User-Movie with 0 rating
def initializeUserItemMap():
	for user in user_set:
		tempItemDict = {}
		for item in item_set:
			tempItemDict[item] = 0
		user_data[user] = tempItemDict
	#print "User-Item map/matrix:"
	#print user_data

# Initialize Movie-User with 0 rating
def initializeItemUserMap():
	for item in item_set:
		tempUserDict = {}
		for user in user_set:
			tempUserDict[user] = 0
		item_data[item] = tempUserDict
	#print "Item-User map/matrix:"
	#print item_data

# Get ratings from data file and update user-movie map/matrix
def prepareUserItemMap():
	data.seek(0) # reset file cursore/iterator
	for line in data:
		temp = line.split("\t")
		user_data[int(temp[0])][int(temp[1])] = int(temp[2])
		#print "adding rating = " + temp[2] + " for movie = " + temp[1] + " to user = " + temp[0]
	#print user_data

# Get ratings from data file and update user-movie map/matrix
def prepareItemUserMap():
	data.seek(0) # reset file cursore/iterator
	for line in data:
		temp = line.split("\t")
		item_data[int(temp[1])][int(temp[0])] = int(temp[2])
		#print "adding rating = " + temp[2] + " for movie = " + temp[1] + " to user = " + temp[0]
	#print user_data

# Master function to calculate UserBasedCF
def calculateUserBasedCF(subject, subjectItem):
	userBasedCFRating = 0
	aveSubjectRating = 0
	sim_prod = 0
	sim_sum = 0
	getTopSimilarNeighbor(subject, subjectItem)
	aveSubjectRating = averageRatingForUser(subject, subjectItem)
	for user in top_similar_users:
		sim_prod = sim_prod + user_sim[subject][user]*(user_data[user][subjectItem]-averageUserRating(user))
		sim_sum = sim_sum + user_sim[subject][user]
	# print sim_prod
	# print sim_sum
	userBasedCFRating = aveSubjectRating + sim_prod/sim_sum
	print "User based Collaborative Filtering for User_id : " + str(subject) + " Movie_id : " + str(subjectItem) + " is :"
	print userBasedCFRating

def calculateItemBasedCF(subject, subjectItem):
	itemBasedCFRating = 0
	aveSubjectRating = 0
	sim_prod = 0
	sim_sum = 0
	getTopSimilarNeighborForMovie(subject, subjectItem)
	aveSubjectRating = averageRatingForMovie(subject, subjectItem)
	for movie in top_similar_movies:
		sim_prod = sim_prod + movie_sim[subject][movie]*(item_data[movie][subjectItem]-averageMovieRating(movie))
		sim_sum = sim_sum + movie_sim[subject][movie]
	# print sim_prod
	# print sim_sum
	itemBasedCFRating = aveSubjectRating + sim_prod/sim_sum
	print "Item based Collaborative Filtering for Movie_id : " + str(subject) + " User_id : " + str(subjectItem) + " is :"
	print itemBasedCFRating

def main():
	args = sys.argv[1:]
	if not args or len(args) != 4:
		print "---------------------------------------------------USAGE-----------------------------------------------------------"
		print "USAGE: python CollaborativeFiltering.py [user-item-rating.data] [user_id] [movie_id] [neighborhood_size]"
		print " - u.data: user-item-rating tab separated data or txt file"
		print " - user_id: int [1-943]"
		print " - movie_id: int [1-1682]"
		print " - neighborhood_size: int"
		print "-------------------------------------------------------------------------------------------------------------------"
		sys.exit(1)
	global data,neighborhood_size
	data = open(args[0], "r")
	neighborhood_size = int(args[3])
	extractData()
	initializeUserItemMap()
	prepareUserItemMap()
	calculateUserBasedCF(int(args[1]), int(args[2]))
	initializeItemUserMap()
	prepareItemUserMap()
	calculateItemBasedCF(int(args[2]), int(args[1]))

if __name__ == "__main__":
	main()

'''
Sample Run:
Ravis-MacBook-Pro:HW4 ravs$ python CollaborativeFiltering.py u.data 192 476 2
Top 2 similar neighbors of subject 192 are:
User 569 with similarity value = 0.424473344739
User 486 with similarity value = 0.415434977233
Average rating for user 192 = 0.0719809637121
Average rating for user 569 = 0.145065398335
Average rating for user 486 = 0.362068965517
User based Collaborative Filtering for User_id : 192 Movie_id : 476 is :
1.30343968052
Top 2 similar neighbors of subject 476 are:
Movie 756 with similarity value = 0.513072356468
Movie 237 with similarity value = 0.496756694081
Average rating for movie 476 = 0.510615711253
Average rating for movie 756 = 0.3934252386
Average rating for movie 237 = 1.51113467656
Item based Collaborative Filtering for Movie_id : 476 User_id : 192 is :
-0.432634911203
'''