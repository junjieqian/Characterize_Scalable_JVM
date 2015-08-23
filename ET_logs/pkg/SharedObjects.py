#!/usr/bin/env Python
# Allocation:
# A <object-id> <size> <type> <thread-id>
# The new object has ID object-id, which is used to refer to the object in later events; the size in bytes; the type (a Java type as a string); the ID of the allocating thread.

# Death:
# D <object-id>
# Pointer update:
# U <old-target-id> <object-id> <new-target-id><thread-id>
# A field (currently, unspecified) in the object with ID object-id is changed from pointing to old-target-id to point to new-target-id, and this occured in thread-id.

# An object-id of 0 indiacates that this is an update to a static field.

# Method entry:
# M <method-id> <receiver-object-id> <thread-id>
# A call to the method method-id with receiver object receiver-object-id in thread thread-id.

# A origin receiver of 0 indicates that this was a static method

# Method exit:
# E <method-id> <receiver-object-id> <thread-id>
# Return from method method-id with receiver object receiver-object-id in thread thread-id.

# A receiver of 0 indicates this was a static method.

import string
import sys

def SharedObjects(filename):
  # capture information from tracefile
  # check each occurence of objects and threads, if always same it isnot shared
  # @param objects, the dict to store the objects associated with thread id
  # @param shared_objects, the list to store the shared objects
  fp = open(filename, 'r')
  objects = {}
  shared_objects = []
  for line in fp:
    word = line.split(' ')
    if word[0] == 'A' or word[0] == 'U':
      object_id = word[1]
      thread_id = word[4]
    elif word[0] == 'M' or word[0] == 'E':
      object_id = word[2]
      thread_id = word[3]
    if object_id != '0':
      if object_id in objects:
        if objects[object_id] != thread_id and (not object_id in shared_objects):
          shared_objects.append(object_id)
      else:
        objects[object_id] = thread_id
  return len(shared_objects)
