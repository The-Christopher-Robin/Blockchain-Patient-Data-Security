pragma solidity ^0.5.16;

contract Health {
    struct Vote {
        address voter;
        string name;
        string age;
        string blood_group;
    }

    mapping(address => bool) public voters;
    mapping(uint256 => Vote) public votes;
    uint256 public voteCount;

    event VoteCast(address indexed voter, string name, string age, string blood_group);

    constructor() public {
        voteCount = 0; // Initialize vote count to 0
    }

    function vote(string memory name, string memory age, string memory blood_group) public {
        require(!voters[msg.sender], "You have already voted.");
        voters[msg.sender] = true;
        votes[voteCount] = Vote(msg.sender, name, age, blood_group);
        voteCount++;
        emit VoteCast(msg.sender, name, age, blood_group);
    }

    function getVote(uint256 index) public view returns (address, string memory, string memory, string memory) {
        require(index < voteCount, "Invalid vote index.");
        Vote memory v = votes[index];
        return (v.voter, v.name, v.age, v.blood_group);
    }
}