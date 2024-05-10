export default function taskBlock(trueOrFalse) {
  const task = false;
  const task2 = true;

  if (trueOrFalse) {
    task = true;
    task2 = false;
  }

  console.log(task, task2);

  return [task, task2];
}
