export const enableDarkmode = (): void => {
  document.body.classList.add("darkmode");
  localStorage.setItem("darkmode", "active");
};

export const disableDarkmode = (): void => {
  document.body.classList.remove("darkmode");
  localStorage.removeItem("darkmode");
};

export const initializeTheme = (): void => {
  const darkmode = localStorage.getItem("darkmode");

  if (darkmode === "active") {
    enableDarkmode();
  } else {
    disableDarkmode();
  }
};

export const toggleTheme = (): void => {
  const darkmode = localStorage.getItem("darkmode");

  if (darkmode !== "active") {
    enableDarkmode();
  } else {
    disableDarkmode();
  }
};
