window.addEventListener("load", function() {
    const loaderFrame = document.getElementById("loading-frame");
    loaderFrame.style.display = "block";
    setTimeout(function(){
        loaderFrame.style.display = "none";
    }, 5000); // 5000ms = 5 seconds
});

let currentIndex = 0;
const storyCards = document.querySelectorAll('.story-card');

function prevStory() {
    if (currentIndex > 0) {
        currentIndex--;
        scrollStoryCarousel();
    }
}

function nextStory() {
    if (currentIndex < storyCards.length - 1) {
        currentIndex++;
        scrollStoryCarousel();
    }
}

function scrollStoryCarousel() {
    const carouselContainer = document.querySelector('.story-carousel');
    const cardWidth = storyCards[currentIndex].offsetWidth;
    const scrollOffset = cardWidth * currentIndex;
    carouselContainer.scrollTo({
        left: scrollOffset,
        behavior: 'smooth'
    });
}

function insertSelectedStory() {
    const selectElement = document.getElementById('storySelect');
    const selectedParagraph = selectElement.value;
    const textareaElement = document.querySelector('textarea[name="text"]');
    textareaElement.value = selectedParagraph;
}

function selectStory(paragraph) {
    const textareaElement = document.querySelector('textarea[name="text"]');
    textareaElement.value = paragraph;
}

function insertStory(paragraph) {
    const textareaElement = document.querySelector('textarea[name="text"]');
    const currentText = textareaElement.value;
    textareaElement.value = currentText + '\n' + paragraph;
}

function toggleStoryCarousel() {
    const storyCheckbox = document.getElementById('storyCheckbox');
    const storyCarousel = document.getElementById('storyCarousel');

    if (storyCheckbox.checked) {
        storyCarousel.classList.remove('hidden');
    } else {
        storyCarousel.classList.add('hidden');
    }
}
