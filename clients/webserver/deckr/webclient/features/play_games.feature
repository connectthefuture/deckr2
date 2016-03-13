Feature: Playing a game

  Scenario: Start a standard game
    Given I have joined a standard game
    When I start the game
    Then the game will be started
      And I will see my nickname

  Scenario: Pass priority
    Given I have started a multiplayer standard game
      And I have priority
    When I pass priority
    Then I will no longer have priority

  Scenario: Play land
    Given I have started a multiplayer standard game with a deck of Forests
      And I have priority
    When I play a land
    Then my land will be on the battlefield
