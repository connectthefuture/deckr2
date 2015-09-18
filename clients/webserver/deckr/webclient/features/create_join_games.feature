Feature: Creating and joining games

  Scenario: Create a standard game
    Given I visit the url "/game/create"
    When I create a standard game
    Then my game will be created
      And my game will appear in the lobby

  Scenario: Joining a standard game I created
    Given I have created a standard game
    When I join the game
    Then I will be in the game room
      And I will see my nickname
