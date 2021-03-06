pragma solidity ^0.4.11;

contract SoftwareTransaction {
//关键字“public”使变量能从合约外部访问。
    address public creator;
    mapping (address => uint) public balances;
    mapping (bytes32 => address) public softwareAuthors;
    mapping (bytes32 => uint) public softwarePrices;
    mapping (bytes32 => string) internal softwareHashes;
    mapping (bytes32 => bool) internal checked;
    uint public balance1; //买家余额
    uint public balance2; //开发者余额
    uint public balance3; //第三方余额
    uint public balance4; //合约押金

//这个构造函数的代码仅仅只在合约创建的时候被运行。
    function SoftwareTransaction() public {
        creator = msg.sender;
        balances[creator] = 100000;
        balance1 = 10000;
    }
    function mint(address receiver, uint amount) public {
        if (msg.sender != creator) return;
        balances[receiver] += amount;
    }

    function send(address receiver, uint amount) public {
        if (balances[msg.sender] < amount) return;
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
    }

    function publish(bytes32 _name, uint _price, string _hash) public {
        require(softwareAuthors[_name] == address(0));
        softwareAuthors[_name] = msg.sender;
        softwarePrices[_name] = _price;
        softwareHashes[_name] = _hash;
    }
    
    function getPrice(bytes32 _name) public returns(uint) {
        require(softwareAuthors[_name] != address(0));
        return softwarePrices[_name];
    }

    function buySoftware(bytes32 _name) public returns(string) {
        require(softwareAuthors[_name] != address(0));
        require(checked[_name] == true);
        if (balances[msg.sender] < softwarePrices[_name]) return "";
        balances[msg.sender] -= softwarePrices[_name];
        balances[softwareAuthors[_name]] += softwarePrices[_name];
        return softwareHashes[_name];
    }

    function varify(bytes32 _name, uint score) public {
        require(softwareAuthors[_name] != address(0));
        require(balance4>=softwarePrices[_name]);
        softwarePrices[_name] = softwarePrices[_name] * score / 10;
        checked[_name] = true;
        balance4 -= softwarePrices[_name];
        balance2 += softwarePrices[_name];
        if (balance4 > 50) {
            balance4 -= 50;
            balance3 += 50;
            balance1 += balance4;
            balance4 = 0;
        } else {
            balance3 += balance4;
            balance4 = 0;
        }
    }
    

    function getBalance() public returns(uint) {
        return balances[msg.sender];
    }

    function deposit(uint amount) public {
        require(balance1>=amount);
        balance1 -= amount;
        balance4 += amount;
    }
}