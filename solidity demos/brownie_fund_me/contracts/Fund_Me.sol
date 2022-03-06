// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
//import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainLink.sol";
contract FundMe {
    
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    
    //$50
    //red means payable function
    // constructor... function that gets called instantly. eg to determine the owner
    address public owner;
    constructor() public {
    owner = msg.sender;

    }

    function fund() public payable {
    uint256 minimumUSD = 50 * 10 ** 18;
    require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH!");  
    addressToAmountFunded[msg.sender] += msg.value;
    funders.push(msg.sender);
    // eth -> usd conversion rate
    }
    //eth - usd address from chainlink page below

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface pricefeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return pricefeed.version();
    }

    function getPrice() public view returns(uint256) {
        AggregatorV3Interface pricefeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
            (, 
            int price,
            ,
            ,
            ) = pricefeed.latestRoundData();
            return uint256(price * 10000000000);
     
    }
    //10000000000
    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount)/ 1000000000000000000;
        return ethAmountInUsd;
    }

    //change function in a declarative way
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function withdraw() payable onlyOwner public {
        
        payable(msg.sender).transfer(address(this).balance); 
        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
    } 
      //Solidity v0.7 syntax
    funders = new address[](0);
}

}