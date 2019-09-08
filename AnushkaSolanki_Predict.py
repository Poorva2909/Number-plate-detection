import AnshulPaliwal
import pickle

print("Finalized model loading…..")
filename = './finalized_model.sav'
f_model = pickle.load(open(filename, 'rb'))

# the finalized_model dumped in training module is opened

print('Successfully loaded.')
set_classified = []
# predicting characters of number plate
for char in SegmentCharacters.ch:
    #converting to 1D array
    char = char.reshape(1, -1);
    rs = f_model.predict(char)
    set_classified.append(rs)

#print('Classification result')
#print(set_classified)

strPlate = ''
for each_set in set_classified:
    strPlate += each_set[0]

#print('Predicted license plate')
#print(strPlate)

# sort the characters from SegmentCharacters to it’s right order
# column_list is used to sort the wrongly arranged letter

copyList = SegmentCharacters.col_l[:]
SegmentCharacters.col_l.sort()
finalPlate_str = ''
for char in SegmentCharacters.col_l:
    finalPlate_str += strPlate[copyList.index(char)]

print('Final License Plate')
print(finalPlate_str)



