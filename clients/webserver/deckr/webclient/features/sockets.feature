Feature: Connecting, and sending messages to Deckr server via Websockets

  Scenario: Test Deckr server connection
    Given I visit the url "/lobby"
    Then I will be connected to the Deckr server
