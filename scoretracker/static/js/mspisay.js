const carouselList = document.querySelector(".circular-carousel__list");
const carouselItems = gsap.utils.toArray(".circular-carousel__item");
const numItems = carouselItems.length;
const empireHeading = document.getElementById("empire-heading");
const contestantNameDisplay = document.getElementById("contestant-name");
const bgGradient = document.querySelector(".bg-gradient");

let lastContestantId = null;

// Throttle function for performance
function throttle(func, delay) {
  let timeoutId;
  let lastExecTime = 0;
  return function(...args) {
    const currentTime = Date.now();
    if (currentTime - lastExecTime < delay) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        lastExecTime = currentTime;
        func.apply(this, args);
      }, delay);
    } else {
      lastExecTime = currentTime;
      func.apply(this, args);
    }
  };
}

// Function to detect which contestant is at the top
function getTopContestant() {
  const rotation = gsap.getProperty(carouselList, "rotation");
  // Negate rotation to reverse direction
  const normalizedRotation = ((-rotation % 360) + 360) % 360;
  const anglePerItem = 360 / numItems;
  const index = Math.round(normalizedRotation / anglePerItem) % numItems;
  return carouselItems[index];
}

// Function to update page theme based on active contestant
function updateTheme() {
  const topItem = getTopContestant();
  const contestantId = topItem.dataset.contestantId;
  
  // Only update if contestant changed
  if (contestantId === lastContestantId) return;
  lastContestantId = contestantId;
  
  const empire = topItem.dataset.empire;
  const contestantName = topItem.dataset.contestantName;
  const contestantData = contestantsData.find(c => c.id == contestantId);
  
  if (contestantData) {
    const empireColor = contestantData.empire_color;
    const empireName = contestantData.empire_display.toUpperCase();
    
    // Update CSS variable
    document.documentElement.style.setProperty('--empire-color', empireColor);
    
    // Update heading text and style
    empireHeading.textContent = empireName;
    empireHeading.style.color = empireColor;
    
    // Update contestant name display with animation re-trigger
    contestantNameDisplay.style.animation = 'none';
    setTimeout(() => {
      contestantNameDisplay.textContent = contestantName;
      contestantNameDisplay.style.color = empireColor;
      contestantNameDisplay.style.animation = 'slideInScale 0.5s ease-out';
    }, 10);
    
    // Update background gradient with empire color
    bgGradient.style.background = `radial-gradient(circle at 50% 0%, ${empireColor}15, #000000 70%)`;
    
    // Dim contestants not from the same empire
    carouselItems.forEach(item => {
      const itemEmpire = item.dataset.empire;
      if (itemEmpire === empire) {
        item.classList.remove('dimmed');
      } else {
        item.classList.add('dimmed');
      }
    });
  }
}

function positionItems() {
  gsap.set(carouselItems, {
    motionPath: {
      path: "#circular-carousel-path",
      align: "#circular-carousel-path",
      alignOrigin: [0.5, 0.5],
      start: -0.25,
      end: (i) => i / numItems - 0.25,
      autoRotate: true
    }
  });
}

const throttledUpdate = throttle(updateTheme, 100);

const draggable = Draggable.create(carouselList, {
  type: "rotation",
  inertia: true,
  throwResistance: 15000,
  maxDuration: 0.3,
  snap: (endVal) => gsap.utils.snap(360 / numItems, endVal),
  onDrag: throttledUpdate,
  onThrowUpdate: throttledUpdate,
  onDragEnd: updateTheme
});

// initial
positionItems();
updateTheme();

window.addEventListener("resize", () => {
  gsap.killTweensOf(carouselItems);
  positionItems();
});