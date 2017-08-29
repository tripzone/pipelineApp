import { observable, action } from "mobx";

export class var1 {
	@observable id = 0;
	@observable name = "";

	constructor(name, id) {
		this.id = id;
		this.name = name;
	}
}

export let count = observable({
	id: 0
});
count.inc = function() {
	this.id = this.id + 1;
};
