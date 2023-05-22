/** @format */

var model
var predResult = document.getElementById('result')
async function initialize() {
  model = await tf.loadLayersModel('model.json')
}
async function predict() {
  // action for the submit button
  let image = document.getElementById('img')
  let tensorImg = tf.browser
    .fromPixels(image)
    .resizeNearestNeighbor([720, 720])
    .toFloat()
    .expandDims()
  prediction = await model.predict(tensorImg).data()
  if (prediction[0] === 0) {
    predResult.innerHTML = "I think it's a cat"
  } else if (prediction[0] === 1) {
    predResult.innerHTML = "I think it's a dog"
  } else {
    predResult.innerHTML = 'This is Something else'
  }
}
initialize()
