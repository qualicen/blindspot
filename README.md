# blindspot
To train a model: 
python blindspot.py train <path/to/training/data> <path/to/param/file> <path/to/output/examples>

To run the prediction webapp compile webapp with

install node.js
install angular-cli with npm install -g @angular/cli
install build-angular npm install --save-dev @angular-devkit/build-angular

- cd webapp
- npm install
- ng build

run the server with python blindspot.py predict_server <path/to/data/file> <path/to/model>
Remark: There are two model files: model.json and model.h5. As parameter just give the model file name without suffix (leave out .h5 and .json)
Remark2: The original datafile is needed to extract the vocabulary and the correct definitions