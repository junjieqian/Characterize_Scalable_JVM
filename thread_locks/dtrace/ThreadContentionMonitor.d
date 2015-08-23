hotspot$target:::monitor-contended-enter
{
	this->threadid = arg0;
	this->monitorid = arg1;
	this->monitorclass = (string)copyin(arg2, arg3+1);
	this->cstart = timestamp;
	printf("Thread %d trying to acquire monitor %d of type %s at %d\n", this->threadid, this->monitorid, this->monitorclass, this->cstart);
}

hotspot$target:::monitor-contended-entered
{
  this->threadid = arg0;
  this->monitorid = arg1;
  this->monitorclass = (string)copyin(arg2, arg3+1);
  this->cstart = timestamp;
  printf("Thread %d entered monitor %d of type %s at %d\n", this->threadid, this->monitorid, this->monitorclass, this->cstart);
}

hotspot$target:::monitor-contended-exit
{
  this->threadid = arg0;
  this->monitorid = arg1;
  this->monitorclass = (string)copyin(arg2, arg3+1);
  this->cstart = timestamp;
  printf("Thread %d exit monitor %d of type %s at %d\n", this->threadid, this->monitorid, this->monitorclass, this->cstart);
}
