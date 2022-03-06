// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;


//contract is class
contract SimpleStorage {

// automatically initialised to 0
    uint256 favnumber;
    bool favBool;
  

//methods
    function store(uint256 _favnumber) public returns(uint256) {
        favnumber = _favnumber;
        return _favnumber;
    }


    struct People {
        uint256 favnumber;
        string name;

    }

    People[] public people;
    mapping(string => uint256) public nameToFavNum;


    People person = People({favnumber:13, name: "Patrick"});

    //view, pure... read state off blockchain
    //blue buttons are view functions, do not change state of BC
    //pure functions purely do math
    function retrieve() public view returns(uint256) {
        return favnumber;
    }

    function addPerson(string memory _name, uint256 _favnumber) public {
        people.push(People(_favnumber, _name));
        nameToFavNum[_name] = _favnumber;
    }
  


}