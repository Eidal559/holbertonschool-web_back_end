export default function taskBlock(trueOrFalse) {
  let task = false;
  let task2 = true;

  if (trueOrFalse) {
	task = true;
	task2 = false;
  }

  console.log(task, task2);

  return [task, task2];
}
