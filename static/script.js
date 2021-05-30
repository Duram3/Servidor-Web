function switchSheet() {
    let theme = document.getElementById("theme");
  
    if (theme.getAttribute("href") == "static/mododia.css") {
      theme.href = "static/modonoche.css";
    } else {
      theme.href = "static/mododia.css";
    }
  }