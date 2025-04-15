nums = [2,2,1,1,1,2,2] 

majority = 1 
majority_count = []

if len(nums) ==0:
    print(0)  
elif len(nums)==1:
    print(nums[0])
else:

    for i in range(0 , len(nums)):
        for j in range(i+1 , len(nums)):
                if nums [i] == nums [j]:
                    majority +=1

        majority_count.append(majority)

        
majority_count.sort()

print(majority_count)
