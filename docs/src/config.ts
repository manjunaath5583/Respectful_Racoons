export const sidebar = [
  {
    text: "Introduction",
    link: "", // No leading slash needed, so this links to the homepage
    children: [
      { text: "Getting around", link: "getting-around" },
      { text: "The main screen", link: "the-main-screen" },
      { text: "The All Modules screen", link: "all-modules-screen" },
      { text: "Editing the settings", link: "settings-toml" },
    ],
  },
  {
    text: "Custom modules",
    link: "modules", // No leading slash needed, so this links to the homepage
    children: [
      { text: "today, card and display", link: "modules/today-card-display" },
      { text: "Listening to keystrokes", link: "modules/keystrokes" },
      { text: "Updates and destroys", link: "modules/update-destroy" },
      { text: "Storing data and settings", link: "modules/data-settings" },
      {
        text: "Contributing your module",
        link: "modules/contributing-modules",
      },
    ],
  },
];
