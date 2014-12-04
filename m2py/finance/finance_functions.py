def AER(Interest, N):
	"""
	Convertes an interest rate to  [A]nnual [E]quivalent [R]ate
	or per year

	Rate 		- Interest Rate
	Compound	- Compound Frequency


	Example:
		EAR(0.1, 12)
		10% per month --->  % per year
		Compounds Frequency = 12 ---> 12 monhts = 1 Year

		Returns = (1+10%)^12 = 12.68%

	"""
	return (1.0+Interest)**N - 1.0


def EAR(APN, N):
	"""
	Returns the EAR given the APN

		APN -- APN Interest Rate
		N   -- Compound Frequency

	Example:
		EAR(0.12, 12)

		12% a year compounded monthly.
		1 y = 12 months ==> N=12

	"""
	return (1.0+ APN/N)**N - 1

