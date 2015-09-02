Feature: Playing a game

  Scenario: Start a standard game
    Given I have joined a standard game
    When I start the game
    Then the game will be started

  Scenario: Pass priority
    Given I have started a standard game
    When I pass priority
    Then I will no longer have priority
