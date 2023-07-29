
document.addEventListener("DOMContentLoaded", function () {
  const splashScreen = document.getElementById("splash-screen");
  function hideSplashScreen() {
    splashScreen.style.display = "none";
  }
  setTimeout(hideSplashScreen, 5000);
});

function startAnimation() {

  const diagonalLine = document.querySelector('.diagonal_line');
  const heatMapDiv = document.getElementById('heat_map');
  
  // Calculate the animation duration in milliseconds (3 seconds)
  const animationDuration = 3000;
  
  // Set the animation properties
  diagonalLine.style.animation = `moveHorizontal ${animationDuration}ms linear`;
  
  // After the animation completes, reset the animation properties
  setTimeout(() => {
    diagonalLine.style.animation = '';
  }, animationDuration);
}

// Call the function to start the animation when the page loads
window.onload = startAnimation;