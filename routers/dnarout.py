from fastapi import APIRouter, HTTPException, Depends
from schemas import schema
from utils import deps

router = APIRouter()


def LinearSearch(lys, element):
    for i in range (len(lys)):
        if lys[i] == element:
            return lys[i]
    return None


def FibonacciSearch(lys, val):
    fibM_minus_2 = 0
    fibM_minus_1 = 1
    fibM = fibM_minus_1 + fibM_minus_2
    while (fibM < len(lys)):
        fibM_minus_2 = fibM_minus_1
        fibM_minus_1 = fibM
        fibM = fibM_minus_1 + fibM_minus_2
    index = -1;
    while (fibM > 1):
        i = min(index + fibM_minus_2, (len(lys)-1))
        if (lys[i] < val):
            fibM = fibM_minus_1
            fibM_minus_1 = fibM_minus_2
            fibM_minus_2 = fibM - fibM_minus_1
            index = i
        elif (lys[i] > val):
            fibM = fibM_minus_2
            fibM_minus_1 = fibM_minus_1 - fibM_minus_2
            fibM_minus_2 = fibM - fibM_minus_1
        else :
            return lys[i]
    if(fibM_minus_1 and index < (len(lys)-1) and lys[index+1] == val):
        return index+1;
    return None


# проверка введенной пользователем последовательности dna
def input_validate(input):
    input = str(input).lower()
    if len(input) != 3:
        return None

    if not all(c.isalpha() for c in input):
        return None

    return str(input).lower()


@router.post("/", status_code=200)
async def send_dna(input: str, current_user: schema.User = Depends(deps.get_current_user)):
    dna = ("tgacccactaatcagcaacatagcactttgagcaaaggcctgtgttggagctattggccc"
        "caaaactgcctttccctaaacagtgttcaccattgtagacctcaccactgttcgcgtaac"
        "aactggcatgtcctgggggttaatactcac")
    kodons = [dna[i:i+3] for i in range(0, len(dna), 3)]
    input = input_validate(input)
    if not input:
        return "Кодон может состоять только из последовательности 3 букв"
    # вариант поиска 1
    if input in kodons:
        return "DNA sequence found"
    
    # вариант поиска 2
    sequence = LinearSearch(kodons, input)
    if sequence:
        return "DNA sequence found"

    # вариант поиска, Метод Фибанначи 3
    sequence2 = FibonacciSearch(kodons, dna)
    if sequence2:
        return "DNA sequence found"
    else:
        return "DNA sequence not found"