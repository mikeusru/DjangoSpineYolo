function changeRating(x, pk) {
    // x.classList.toggle("fa-thumbs-down");
    console.log("changing rating of " + pk);
    ratingSocket.send(JSON.stringify({
        'type': 'rating_toggle',
        'pk': pk
    }));
}

function getRatingClass(rating) {
    console.log("rating is " + rating);
    return ("fa fa-thumbs-" + (rating ? 'up' : 'down'))
}