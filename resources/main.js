//
// Themes
//
function setTheme(newtheme=null){
	if (newtheme == null){
		newtheme = document.documentElement.classList.contains("darktheme") ? "light" : "dark";
	}

	if (newtheme == "light"){
		document.documentElement.classList.remove("darktheme");
		localStorage.setItem('theme', 'light');
	} else {
		document.documentElement.classList.add("darktheme");
		localStorage.setItem('theme', 'dark');
	}

	document.querySelector("meta[name='theme-color']").content = getComputedStyle(document.documentElement).getPropertyValue('--color-background').trim();
}

// Set initial theme
if (localStorage['theme'] == null){
	if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches){
		setTheme('dark');
	} else {
		setTheme('light');
	}
	
} else {
	setTheme(localStorage.getItem('theme'));
}

// Change theme when OS theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {setTheme(event.matches ? "dark" : "light");});


// Defered

 window.addEventListener ('load', function () {
	// Animations
	const options = {root: null, rootMargin: '0px', threshold: 0};
	const observer = new IntersectionObserver((entries, observer) => {
		entries.forEach((entry) => {
			if (entry.isIntersecting){
				entry.target.classList.add("animation");
			} else {
				<!-- entry.target.classList.remove("animation"); -->
			}
		});
	}, options);

	for (var card of document.querySelectorAll(".card")){
		observer.observe(card);
	}

	// Themes
	document.getElementById("themetoggle").addEventListener("click", function(){setTheme();});

 });