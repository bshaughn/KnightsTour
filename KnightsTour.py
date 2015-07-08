# Bart Shaughnessy 2015
# Solves a Knights Tour puzzle for a user-specified NxM chessboard
# Knights Tour involves moving a single Knight around an empty chessboard
#  only landing in each space one time

# This program allows the user to specify chessboard dimensions,
#   and then uses the findPath() method to solve the puzzle. 
# Knight starts in upper left corner. 

# Example usage:
#   import KnightsTour as kt
#   myboard = kt.chessboard(8,8)
#   myboard.findPath()

# Please note: program will fail for recursion depth for large chessboards (>25x25)
#  Also seems to slow down for >=10x10

import math
from array import array
from sys import stdout

class chessboard:
	def __init__(self, length, width):
		self.width = width
		self.length = length
		self.max = self.length * self.width
		self.open_spaces = self.max - 1
		self.spaces = []
		self.lastPos = []
		for i in range(0, self.max):
			self.spaces.append(0)
			self.lastPos.append(0)
			
		#print "length of spaces array is: ", len(self.spaces)
		#print "length of lastPos array is: ", len(self.lastPos)
	
	# finds legal moves from a given space on the chessboard
	#  Prioritizes spaces on the outer edges of the chessboard
	#  (This seems to drastically improve algorithm performance)	
	def findMoves(self, currPos):
		moves = []
		col = currPos % self.width
		row = int(math.floor(currPos/self.width))

		if col>1:
			col -= 2
			if ((row-1)>=0) and (self.spaces[col+((row-1)*self.width)]==0):
				if (col==0  or (row-1)==0):
					moves.append(col+((row-1)*self.width))
				else:
					moves.insert(0,col+((row-1)*self.width))
			if ((row+1)<self.length) and (self.spaces[col+((row+1)*self.width)]==0):
				if (col==0 or (row+1)==self.length-1):
					moves.append(col+((row+1)*self.width))
				else:
					moves.insert(0,col+((row+1)*self.width))
			col += 2
		if row>1:
			row -= 2
			if (col>0) and (self.spaces[(self.width*row)+col-1]==0):
				if (row==0 or col==0):
					moves.append((self.width*row)+col-1)
				else:
					moves.insert(0,(self.width*row)+col-1)
			if ((col+1)<self.width) and (self.spaces[(self.width*row)+col+1]==0):
				if (row==0 or (col+1)==self.width-1):
					moves.append((self.width*row)+col+1)
				else:
					moves.insert(0,(self.width*row)+col+1)
			row += 2
		if col<(self.width-2):
			col += 2
			if ((row-1) >= 0) and (self.spaces[col+((row-1)*self.width)]==0):
				if (col == self.width-1 or (row-1)==0):
					moves.append(col+((row-1)*self.width))
				else:
					moves.insert(0,col+((row-1)*self.width))
			if ((row+1)<self.length) and (self.spaces[col+((row+1)*self.width)]==0):
				if ((row+1)==(self.length-1) or col==self.width-1):
					moves.append(col+((row+1)*self.width))
				else:
					moves.insert(0,col+((row+1)*self.width))
			col -= 2
		if row<(self.length-2):
			row += 2
			if (col>0) and (self.spaces[(self.width*row)+col-1]==0):
				if (row==(self.length-1) or ((col-1)==0)):
					moves.append((self.width*row)+col-1)
				else:
					moves.insert(0,(self.width*row)+col-1)
			if ((col+1)<self.width) and (self.spaces[(self.width*row)+col+1]==0):
				if (row==(self.length-1) or (col+1)==(self.width-1)):
					moves.append((self.width*row)+col+1)
				else:
					moves.insert(0,(self.width*row)+col+1)
			row -= 2

		return moves
	
	# Moves the Knight on the Chessboard
	#  Uses Recursive backtracking to explore each possible move from a given space
	#  Receives current position and computes a list of available spaces
	#  Moves in order, taking the last available space
	#  If no moves are available, the function recurses to the last position
	#    and continues from the next available space. 			
	def moveKnight(self, currPos):
		self.spaces[currPos] = self.max - self.open_spaces
		self.open_spaces -= 1
		
		# print "Moveknight currPos: ",currPos
		# print "Previous position: ",self.lastPos[currPos]
		# print "open spaces: ", self.open_spaces
		# for i in range(0, self.length):
		#  		for j in range(0, self.width):
		#  			print self.spaces[j+(i*self.width)]," ",
		#  		print "\n"

		progress = ""
		for i in range(self.open_spaces):
			progress += "+"
		for j in range(self.max - self.open_spaces-1):
			progress += "-"

		print "\r"+progress,
		stdout.flush()

			
		if (self.open_spaces == -1):
			self.spaces[currPos] = self.max
			return "DONE"
		
		possible_moves = self.findMoves(currPos)
		# print "Moves array: ",
		# for i in possible_moves:
		# 	print i, " ",
				
		# print "\n"
		
		pmc = len(possible_moves)
		while (pmc != 0):
			nextPos = possible_moves.pop()
			#print "\n"
			#print "Picked ", nextPos, " as the next move"
			self.lastPos[nextPos] = currPos
			outcome = self.moveKnight(nextPos)
			if (outcome == "DONE"):
				return "DONE"
			elif (outcome == "No Moves Left"):
				return "No Moves Left"
			pmc -= 1
			
		if (pmc == 0) and (currPos == 0):
			return "No Moves Left"
			
		self.open_spaces += 1
		self.spaces[currPos] = 0
		#print "Recursing to ", self.lastPos[currPos]		
		return
		
	def findPath(self):
		result = self.moveKnight(0)
		if (result == "No Moves Left"):
			print "No Solution for this board configuration"
			return
		
		elif (result == "DONE"):
			print "\n"
			for i in range(0, self.length):
				for j in range(0, self.width):
					print self.spaces[j+(i*self.width)]," ",
				print "\n"
			return
		else:
			print "Mysterious error occurred!"
		