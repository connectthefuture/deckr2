Feature: Accessing static pages

  Scenario: Accessing the home page
    Given I visit the url "/"
    Then I see "Welcome to Deckr!"

  Scenario: Accessing the lobby
    Given I visit the url "/lobby"
    Then I see "Deckr Lobby"
