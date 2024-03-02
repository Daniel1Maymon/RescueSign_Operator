// JavaScript code to display one image at a time and provide navigation


var imageUrls = null;
// Get the chosen option element by its ID
var chosenOption = document.getElementById('chosen-option');

var waitingMsg = document.getElementById('waiting-msg')

// Get the image container element by its ID
var imageContainer = document.getElementById('image-container');

// Hide the image container initially
imageContainer.style.display = 'none';
waitingMsg.style.display = 'none'

// Get the current image element by its ID
var currentImage = document.getElementById('current-image');

// Buttons:
var prevButton = document.getElementById('prev-button');
var nextButton = document.getElementById('next-button');
var turnSirenButton = document.getElementById('TurnSiren')
var keepMovingButton = document.getElementById('keepMoving')

var currentIndex = 1; // Index of the currently displayed image

function getImagesUrls() {
    return new Promise(function (resolve, reject) {
        console.log('::: function getImagesUrls():::')

        fetch('/get_images_urls', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(data => {
                imageUrls = data;
                console.log("imageUrls = ", imageUrls)
                currentIndex = 0;
                // return imageUrls;
                resolve(imageUrls);
            })
            .catch(error => {
                console.log('Error: ', error)
            })

        if (imageUrls !== null) {
            console.log("imageUrls = ", imageUrls)
        }
        else {
            console.log("imageUrl is null")
        }
    });
}

function openSocket() {
    waitingMsg.style.display = 'block';

    imageUrls = null
    console.log("::: OpenSocket Button clicked :::")

    fetch(
        '/create_socket_connection', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {

            imageContainer.style.display = 'block';
            waitingMsg.style.display = 'none'
            // Start displaying the images

            console.log(":: Before getImagesUrls() ::")
            getImagesUrls().then(function (result) {
                imageUrls = result;
                console.log(" :: imageUrls = ", imageUrls);
                updateImage();
            })
            console.log(":: AFTER getImagesUrls() ::")
            // imageUrls = getImagesUrls();
            // // handleNextButtonClick();
            // updateImage();

            // // console.log(":: imageUrls: ", imageUrls)
            // if (imageUrls !== null) {
            //     console.log("imageUrls is not null = ", imageUrls)
            //     // updateImage();

            // }
            // else {
            //     console.log("imageUrls is null");
            //     // updateImage();
            // }

        })

}

function isImageBroken(imageSrc) {

    return new Promise((resolve) => {
        const img = new Image();

        img.addEventListener('load', () => {
            resolve(false); // Image loaded successfully
        });

        img.addEventListener('error', () => {
            resolve(true); // Image failed to load
        });
        console.log(":: isImageBroken ::")
        img.src = imageSrc;
    })
}

// Function to update the displayed image
function updateImage() {

    currentImage.src = imageUrls[currentIndex];
    console.log('currentIndex = ', currentIndex)
    console.log('currentImage.src = ', currentImage.src)

    // if (imageUrls !== null) {
    //     handleNextButtonClick()
    //     // isImageBroken(imageUrls[currentIndex]).then((isBroken) => {
    //     //     if (isBroken) {
    //     //         currentIndex++;
    //     //         console.log("currentImage.src is null")
    //     //     } else {
    //     //         
    //     //         console.log("currentImage.src = ", currentImage.src)
    //     //     }
    //     // })

    // } else {
    //     console.log(" updateImage():: imageUrls is null")
    // }

}

// Function to handle the previous button click
function handlePrevButtonClick() {
    console.log(":: (handleNextButtonClick) :: currentIndex = ", currentIndex)
    if (currentIndex > 0) {
        currentIndex--;
    } else {
        currentIndex = imageUrls.length - 1;
    }
    updateImage();
}

// Function to handle the next button click
function handleNextButtonClick() {
    console.log(":: (handleNextButtonClick) :: currentIndex = ", currentIndex)
    if (currentIndex < imageUrls.length - 1) {
        currentIndex++;
    } else {
        currentIndex = 0;
    }
    updateImage();
}


function deleteAllFiles() {
    console.log("::::::: deleteAllFiles()")
    fetch('/delete_oldest_frames')
        .then(response => response.json())
        .then(data => {
            console.log('response from /delete_oldest_frames: ', data)
        })
        .catch(error => {
            console.error('Error: ', error)
        })
}


function operatorResponse(response) {

    console.log("::: operatorResponse START ")
    console.log("response = ", response)
    // Handle operator responses here
    imageContainer.style.display = 'none';
    waitingMsg.style.display = 'none'

    var selectedOption = event.target;
    console.log("selectedOption = ", selectedOption)
    selectedOption.style.color = "red";

    // Remove the class after a timeout
    setTimeout(
        function () {
            selectedOption.style.color = ""; // Reset to default color (inherit or initial)
        }, 3000)

    imageUrls = null;
    deleteAllFiles()

    console.log(":::: Operator response: " + response);

    // Make an HTTP POST request to send the response to the server
    fetch('http://127.0.0.1:44444/response_from_operator', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ answer: response })
    })
        .then(response => {
            // Handle the server response here if needed 
            console.log('Server response:', response);
            console.log("delete frames")

            // Start displaying the images
            // updateImage();
        })
        .catch(error => {
            // Handle any error that occurs during the request
            console.error('Error:', error);
        });

    waitingMsg.style.display = 'block'


    // waiting for new video - Trying to connect to the model socket
    openSocket()
}

// Add event listeners to the buttons
prevButton.addEventListener('click', handlePrevButtonClick);
nextButton.addEventListener('click', handleNextButtonClick);
turnSirenButton.onclick = function () {
    operatorResponse('Turn on siren');
}

keepMovingButton.onclick = function () {
    operatorResponse('Keep moving')
}

// updateImage()
// Call the openSocket function to establish the socket connection
// openSocket();