export default function taskBlock(trueOrFalse) {
	let task = false;
	let task2 = true;

	if (trueOrFalse) {
	  /*eslint-disable */
	  task = true;
	  task2 = false;
	}

	return [task, task2];
  }
